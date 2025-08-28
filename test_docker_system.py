"""
Script de pruebas automatizadas para el sistema Docker de IA-AGENTS
"""
import requests
import time
import json
import docker
from datetime import datetime
import subprocess
import sys
import os

class DockerTradingTestSuite:
    def __init__(self):
        self.base_url = "http://localhost:8000/api"
        self.docker_client = docker.from_env()
        self.test_results = []
        self.containers_status = {}
    
    def log_test(self, test_name, success, details=None):
        """Registra resultado de una prueba"""
        result = {
            "test": test_name,
            "success": success,
            "timestamp": datetime.now(),
            "details": details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"    Detalles: {details}")
    
    def check_docker_running(self):
        """Verifica que Docker esté corriendo"""
        try:
            self.docker_client.ping()
            self.log_test("Docker Engine Status", True, "Docker está corriendo")
            return True
        except Exception as e:
            self.log_test("Docker Engine Status", False, f"Docker no está corriendo: {e}")
            return False
    
    def check_containers_status(self):
        """Verifica el estado de todos los contenedores"""
        expected_containers = [
            "ia-agents-api",
            "ia-agents-postgres", 
            "ia-agents-redis",
            "ia-agents-n8n",
            "ia-agents-ollama"
        ]
        
        all_running = True
        
        for container_name in expected_containers:
            try:
                container = self.docker_client.containers.get(container_name)
                status = container.status
                self.containers_status[container_name] = status
                
                if status == "running":
                    self.log_test(f"Container {container_name}", True, f"Estado: {status}")
                else:
                    self.log_test(f"Container {container_name}", False, f"Estado: {status}")
                    all_running = False
                    
            except docker.errors.NotFound:
                self.log_test(f"Container {container_name}", False, "Contenedor no encontrado")
                all_running = False
            except Exception as e:
                self.log_test(f"Container {container_name}", False, f"Error: {e}")
                all_running = False
        
        return all_running
    
    def wait_for_services(self, max_wait=120):
        """Espera a que todos los servicios estén listos"""
        print(f"⏳ Esperando a que los servicios estén listos (máx {max_wait}s)...")
        
        services_to_check = [
            ("API", "http://localhost:8000/api/health"),
            ("PostgreSQL", "tcp://localhost:5432"),
            ("Redis", "tcp://localhost:6379"),
            ("n8n", "http://localhost:5678"),
        ]
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            all_ready = True
            
            # Verificar API
            try:
                response = requests.get("http://localhost:8000/api/health", timeout=5)
                api_ready = response.status_code == 200
            except:
                api_ready = False
            
            if not api_ready:
                all_ready = False
            
            # Verificar PostgreSQL usando docker exec
            try:
                result = subprocess.run([
                    "docker", "exec", "ia-agents-postgres", 
                    "pg_isready", "-U", "ia_user", "-d", "ia_agents"
                ], capture_output=True, timeout=5)
                postgres_ready = result.returncode == 0
            except:
                postgres_ready = False
            
            if not postgres_ready:
                all_ready = False
            
            # Verificar Redis
            try:
                result = subprocess.run([
                    "docker", "exec", "ia-agents-redis", 
                    "redis-cli", "ping"
                ], capture_output=True, timeout=5)
                redis_ready = result.returncode == 0 and b"PONG" in result.stdout
            except:
                redis_ready = False
            
            if not redis_ready:
                all_ready = False
            
            if all_ready:
                self.log_test("Services Ready", True, f"Todos los servicios listos en {time.time() - start_time:.1f}s")
                return True
            
            print(".", end="", flush=True)
            time.sleep(2)
        
        self.log_test("Services Ready", False, f"Timeout después de {max_wait}s")
        return False
    
    def test_api_endpoints(self):
        """Prueba los endpoints principales de la API"""
        endpoints_to_test = [
            ("Health Check", "GET", "/health"),
            ("Paper Trading Portfolio", "GET", "/paper-trading/portfolio"),
            ("Learning Performance", "GET", "/learning/performance"),
            ("Trading Klines", "GET", "/trading/klines?symbol=BTCUSDT&interval=1m&limit=5"),
        ]
        
        all_passed = True
        
        for name, method, endpoint in endpoints_to_test:
            try:
                url = f"{self.base_url}{endpoint}"
                
                if method == "GET":
                    response = requests.get(url, timeout=10)
                elif method == "POST":
                    response = requests.post(url, json={}, timeout=10)
                
                success = response.status_code in [200, 201]
                details = f"Status: {response.status_code}"
                
                if success and endpoint == "/health":
                    # Verificar contenido del health check
                    data = response.json()
                    if data.get("status") == "healthy":
                        details += " - Sistema saludable"
                    else:
                        success = False
                        details += " - Sistema no saludable"
                
                self.log_test(f"API {name}", success, details)
                
                if not success:
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"API {name}", False, f"Error: {e}")
                all_passed = False
        
        return all_passed
    
    def test_paper_trading_cycle(self):
        """Prueba un ciclo completo de paper trading"""
        try:
            # 1. Reset portfolio
            reset_response = requests.post(f"{self.base_url}/paper-trading/reset", 
                                         json={"new_balance": 10000.0})
            
            if reset_response.status_code != 200:
                self.log_test("Paper Trading Cycle", False, "Error en reset")
                return False
            
            # 2. Verificar portfolio inicial
            portfolio_response = requests.get(f"{self.base_url}/paper-trading/portfolio")
            if portfolio_response.status_code != 200:
                self.log_test("Paper Trading Cycle", False, "Error obteniendo portfolio")
                return False
            
            portfolio = portfolio_response.json()
            if portfolio.get("initial_balance") != 10000.0:
                self.log_test("Paper Trading Cycle", False, "Balance inicial incorrecto")
                return False
            
            # 3. Colocar orden de compra
            buy_order = {
                "symbol": "BTCUSDT",
                "side": "BUY", 
                "quantity": 0.001,
                "order_type": "MARKET"
            }
            
            buy_response = requests.post(f"{self.base_url}/paper-trading/order", json=buy_order)
            if buy_response.status_code != 200:
                self.log_test("Paper Trading Cycle", False, "Error en orden de compra")
                return False
            
            buy_result = buy_response.json()
            if buy_result.get("status") != "FILLED":
                self.log_test("Paper Trading Cycle", False, "Orden de compra no ejecutada")
                return False
            
            # 4. Verificar posición
            time.sleep(1)
            portfolio_response = requests.get(f"{self.base_url}/paper-trading/portfolio")
            portfolio = portfolio_response.json()
            
            if len(portfolio.get("positions", [])) == 0:
                self.log_test("Paper Trading Cycle", False, "No se creó posición")
                return False
            
            # 5. Colocar orden de venta
            sell_order = {
                "symbol": "BTCUSDT",
                "side": "SELL",
                "quantity": 0.001,
                "order_type": "MARKET"
            }
            
            sell_response = requests.post(f"{self.base_url}/paper-trading/order", json=sell_order)
            if sell_response.status_code != 200:
                self.log_test("Paper Trading Cycle", False, "Error en orden de venta")
                return False
            
            sell_result = sell_response.json()
            if sell_result.get("status") != "FILLED":
                self.log_test("Paper Trading Cycle", False, "Orden de venta no ejecutada")
                return False
            
            self.log_test("Paper Trading Cycle", True, "Ciclo completo exitoso")
            return True
            
        except Exception as e:
            self.log_test("Paper Trading Cycle", False, f"Error: {e}")
            return False
    
    def test_learning_system(self):
        """Prueba el sistema de aprendizaje"""
        try:
            # Registrar un trade de prueba
            trade_data = {
                "trade_id": "test_trade_docker_001",
                "symbol": "BTCUSDT",
                "side": "BUY",
                "entry_price": 50000.0,
                "exit_price": 51000.0,
                "quantity": 0.001,
                "hold_time_minutes": 30,
                "market_conditions": {
                    "volatility_level": "MEDIUM",
                    "trend_strength": "STRONG_BULLISH",
                    "volume_ratio": 1.2
                },
                "decision_confidence": 0.75
            }
            
            response = requests.post(f"{self.base_url}/learning/record-trade", json=trade_data)
            
            if response.status_code != 200:
                self.log_test("Learning System", False, "Error registrando trade")
                return False
            
            # Obtener performance
            perf_response = requests.get(f"{self.base_url}/learning/performance")
            if perf_response.status_code != 200:
                self.log_test("Learning System", False, "Error obteniendo performance")
                return False
            
            # Evaluar decisión de trading
            eval_data = {
                "market_conditions": {
                    "volatility_level": "HIGH",
                    "trend_strength": "STRONG_BULLISH"
                },
                "signal_confidence": 0.8
            }
            
            eval_response = requests.post(f"{self.base_url}/learning/evaluate-trade", json=eval_data)
            if eval_response.status_code != 200:
                self.log_test("Learning System", False, "Error evaluando decisión")
                return False
            
            eval_result = eval_response.json()
            if "should_trade" not in eval_result:
                self.log_test("Learning System", False, "Respuesta de evaluación incompleta")
                return False
            
            self.log_test("Learning System", True, "Sistema de aprendizaje funcionando")
            return True
            
        except Exception as e:
            self.log_test("Learning System", False, f"Error: {e}")
            return False
    
    def test_database_connectivity(self):
        """Prueba la conectividad con la base de datos"""
        try:
            # Usar docker exec para probar conectividad directa
            result = subprocess.run([
                "docker", "exec", "ia-agents-postgres",
                "psql", "-U", "ia_user", "-d", "ia_agents", "-c", 
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Extraer número de tablas
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines:
                    if line.strip().isdigit():
                        table_count = int(line.strip())
                        if table_count > 0:
                            self.log_test("Database Connectivity", True, f"{table_count} tablas encontradas")
                            return True
                
                self.log_test("Database Connectivity", False, "No se encontraron tablas")
                return False
            else:
                self.log_test("Database Connectivity", False, f"Error de conexión: {result.stderr}")
                return False
                
        except Exception as e:
            self.log_test("Database Connectivity", False, f"Error: {e}")
            return False
    
    def run_performance_benchmark(self):
        """Ejecuta benchmark de performance"""
        try:
            print("\n🚀 Ejecutando benchmark de performance...")
            
            start_time = time.time()
            
            # Múltiples requests concurrentes
            import concurrent.futures
            import threading
            
            def make_request():
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=5)
                    return response.status_code == 200
                except:
                    return False
            
            # Ejecutar 20 requests concurrentes
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(make_request) for _ in range(20)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            end_time = time.time()
            
            success_rate = sum(results) / len(results)
            total_time = end_time - start_time
            requests_per_second = len(results) / total_time
            
            benchmark_success = success_rate >= 0.9 and requests_per_second >= 5
            
            details = f"Success: {success_rate:.2%}, RPS: {requests_per_second:.1f}, Tiempo: {total_time:.2f}s"
            self.log_test("Performance Benchmark", benchmark_success, details)
            
            return benchmark_success
            
        except Exception as e:
            self.log_test("Performance Benchmark", False, f"Error: {e}")
            return False
    
    def run_full_test_suite(self):
        """Ejecuta la suite completa de pruebas para Docker"""
        print("🐳 IA-AGENTS Docker Testing Suite")
        print("=" * 50)
        
        # 1. Verificar Docker
        if not self.check_docker_running():
            print("❌ Docker no está corriendo. Instala e inicia Docker Desktop.")
            return
        
        # 2. Verificar contenedores
        print("\n=== ESTADO DE CONTENEDORES ===")
        containers_ok = self.check_containers_status()
        
        # 3. Esperar servicios
        print("\n=== INICIALIZACIÓN DE SERVICIOS ===")
        if not self.wait_for_services():
            print("⚠️ Algunos servicios no respondieron a tiempo")
        
        # 4. Pruebas de API
        print("\n=== PRUEBAS DE API ===")
        self.test_api_endpoints()
        
        # 5. Pruebas de base de datos
        print("\n=== PRUEBAS DE BASE DE DATOS ===")
        self.test_database_connectivity()
        
        # 6. Pruebas de Paper Trading
        print("\n=== PRUEBAS DE PAPER TRADING ===")
        self.test_paper_trading_cycle()
        
        # 7. Pruebas de Learning
        print("\n=== PRUEBAS DE LEARNING ===")
        self.test_learning_system()
        
        # 8. Benchmark de performance
        print("\n=== BENCHMARK DE PERFORMANCE ===")
        self.run_performance_benchmark()
        
        # 9. Resumen final
        self.print_test_summary()
        self.print_docker_info()
    
    def print_test_summary(self):
        """Imprime resumen de las pruebas"""
        print("\n" + "="*50)
        print("📊 RESUMEN DE PRUEBAS DOCKER")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["success"]])
        failed_tests = total_tests - passed_tests
        
        print(f"Total de pruebas: {total_tests}")
        print(f"✅ Exitosas: {passed_tests}")
        print(f"❌ Fallidas: {failed_tests}")
        print(f"📈 Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ PRUEBAS FALLIDAS:")
            for test in self.test_results:
                if not test["success"]:
                    print(f"  - {test['test']}: {test.get('details', 'Sin detalles')}")
    
    def print_docker_info(self):
        """Imprime información útil de Docker"""
        print("\n🐳 INFORMACIÓN DE CONTENEDORES:")
        print("-" * 30)
        
        services_info = {
            "API": "http://localhost:8000",
            "API Docs": "http://localhost:8000/docs",
            "n8n": "http://localhost:5678 (admin/n8n_password)",
            "Jupyter": "http://localhost:8888 (token: jupyter_token_123)",
            "Grafana": "http://localhost:3000 (admin/grafana_admin)",
            "Prometheus": "http://localhost:9090"
        }
        
        for service, url in services_info.items():
            print(f"  {service}: {url}")
        
        print("\n🔧 COMANDOS ÚTILES:")
        print("  Ver logs de API:        docker logs ia-agents-api -f")
        print("  Ver logs de PostgreSQL: docker logs ia-agents-postgres -f")
        print("  Reiniciar API:          docker restart ia-agents-api")
        print("  Parar todo:             docker-compose down")
        print("  Iniciar todo:           docker-compose up -d")


def main():
    """Función principal"""
    test_suite = DockerTradingTestSuite()
    test_suite.run_full_test_suite()


if __name__ == "__main__":
    main()
