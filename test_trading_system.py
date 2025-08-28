"""
Script de pruebas automatizadas para el sistema de paper trading y aprendizaje
"""
import requests
import time
import json
from datetime import datetime
import random

class TradingTestSuite:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.symbols = ["BTCUSDT", "ETHUSDT"]
        self.test_results = []
    
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
    
    def test_health_check(self):
        """Prueba que la API esté funcionando"""
        try:
            response = requests.get(f"{self.base_url}/health")
            success = response.status_code == 200
            self.log_test("Health Check", success, response.json() if success else response.text)
            return success
        except Exception as e:
            self.log_test("Health Check", False, str(e))
            return False
    
    def test_paper_trading_reset(self):
        """Prueba resetear el portfolio"""
        try:
            response = requests.post(f"{self.base_url}/paper-trading/reset", 
                                   json={"new_balance": 10000.0})
            success = response.status_code == 200
            self.log_test("Paper Trading Reset", success, response.json() if success else response.text)
            return success
        except Exception as e:
            self.log_test("Paper Trading Reset", False, str(e))
            return False
    
    def test_get_portfolio(self):
        """Prueba obtener portfolio inicial"""
        try:
            response = requests.get(f"{self.base_url}/paper-trading/portfolio")
            success = response.status_code == 200
            
            if success:
                portfolio = response.json()
                expected_balance = portfolio.get("initial_balance") == 10000.0
                success = success and expected_balance
            
            self.log_test("Get Portfolio", success, response.json() if success else response.text)
            return success
        except Exception as e:
            self.log_test("Get Portfolio", False, str(e))
            return False
    
    def test_place_buy_order(self, symbol="BTCUSDT", quantity=0.001):
        """Prueba colocar una orden de compra"""
        try:
            order_data = {
                "symbol": symbol,
                "side": "BUY",
                "quantity": quantity,
                "order_type": "MARKET"
            }
            
            response = requests.post(f"{self.base_url}/paper-trading/order", json=order_data)
            success = response.status_code == 200
            
            if success:
                result = response.json()
                success = result.get("status") == "FILLED"
            
            self.log_test(f"Place BUY Order ({symbol})", success, response.json() if success else response.text)
            return success, response.json() if success else None
        except Exception as e:
            self.log_test(f"Place BUY Order ({symbol})", False, str(e))
            return False, None
    
    def test_place_sell_order(self, symbol="BTCUSDT", quantity=0.001):
        """Prueba colocar una orden de venta"""
        try:
            order_data = {
                "symbol": symbol,
                "side": "SELL",
                "quantity": quantity,
                "order_type": "MARKET"
            }
            
            response = requests.post(f"{self.base_url}/paper-trading/order", json=order_data)
            success = response.status_code == 200
            
            if success:
                result = response.json()
                success = result.get("status") == "FILLED"
            
            self.log_test(f"Place SELL Order ({symbol})", success, response.json() if success else response.text)
            return success, response.json() if success else None
        except Exception as e:
            self.log_test(f"Place SELL Order ({symbol})", False, str(e))
            return False, None
    
    def test_learning_record_trade(self, buy_order, sell_order):
        """Prueba registrar un trade en el sistema de aprendizaje"""
        try:
            # Simular datos de mercado
            market_conditions = {
                "volatility_level": "MEDIUM",
                "volatility_value": 2.5,
                "trend_strength": "STRONG_BULLISH",
                "volume_ratio": 1.3,
                "rsi": 45
            }
            
            trade_data = {
                "trade_id": buy_order.get("order_id", "test_trade_001"),
                "symbol": "BTCUSDT",
                "side": "BUY",
                "entry_price": buy_order.get("filled_price", 50000),
                "exit_price": sell_order.get("filled_price", 51000),
                "quantity": 0.001,
                "hold_time_minutes": 30,
                "market_conditions": market_conditions,
                "decision_confidence": 0.75
            }
            
            response = requests.post(f"{self.base_url}/learning/record-trade", json=trade_data)
            success = response.status_code == 200
            
            self.log_test("Learning Record Trade", success, response.json() if success else response.text)
            return success
        except Exception as e:
            self.log_test("Learning Record Trade", False, str(e))
            return False
    
    def test_learning_evaluation(self):
        """Prueba la evaluación de decisiones de trading"""
        try:
            evaluation_data = {
                "market_conditions": {
                    "volatility_level": "HIGH",
                    "volatility_value": 3.2,
                    "trend_strength": "STRONG_BULLISH",
                    "volume_ratio": 1.8,
                    "rsi": 35
                },
                "signal_confidence": 0.8
            }
            
            response = requests.post(f"{self.base_url}/learning/evaluate-trade", json=evaluation_data)
            success = response.status_code == 200
            
            if success:
                result = response.json()
                has_decision = "should_trade" in result
                success = success and has_decision
            
            self.log_test("Learning Evaluation", success, response.json() if success else response.text)
            return success
        except Exception as e:
            self.log_test("Learning Evaluation", False, str(e))
            return False
    
    def test_get_learning_performance(self):
        """Prueba obtener métricas de performance"""
        try:
            response = requests.get(f"{self.base_url}/learning/performance")
            success = response.status_code == 200
            
            self.log_test("Get Learning Performance", success, response.json() if success else response.text)
            return success
        except Exception as e:
            self.log_test("Get Learning Performance", False, str(e))
            return False
    
    def test_trading_endpoints(self):
        """Prueba endpoints de trading existentes"""
        try:
            # Probar obtener klines
            response = requests.get(f"{self.base_url}/trading/klines?symbol=BTCUSDT&interval=1m&limit=10")
            klines_success = response.status_code == 200
            self.log_test("Get Klines", klines_success, f"Data points: {len(response.json().get('data', []))}" if klines_success else response.text)
            
            return klines_success
        except Exception as e:
            self.log_test("Trading Endpoints", False, str(e))
            return False
    
    def run_complete_trading_cycle(self):
        """Ejecuta un ciclo completo de trading con aprendizaje"""
        print("\n🔄 Ejecutando ciclo completo de trading...")
        
        # 1. Colocar orden de compra
        buy_success, buy_order = self.test_place_buy_order("BTCUSDT", 0.001)
        if not buy_success:
            return False
        
        # 2. Esperar un poco
        time.sleep(2)
        
        # 3. Colocar orden de venta
        sell_success, sell_order = self.test_place_sell_order("BTCUSDT", 0.001)
        if not sell_success:
            return False
        
        # 4. Registrar el trade en aprendizaje
        learning_success = self.test_learning_record_trade(buy_order, sell_order)
        
        # 5. Verificar portfolio
        portfolio_success = self.test_get_portfolio()
        
        return buy_success and sell_success and learning_success and portfolio_success
    
    def run_stress_test(self, num_cycles=5):
        """Ejecuta múltiples ciclos de trading para stress test"""
        print(f"\n⚡ Ejecutando stress test con {num_cycles} ciclos...")
        
        successful_cycles = 0
        
        for i in range(num_cycles):
            print(f"\n--- Ciclo {i+1}/{num_cycles} ---")
            
            # Variar parámetros para cada ciclo
            symbol = random.choice(self.symbols)
            quantity = round(random.uniform(0.0005, 0.002), 6)
            
            # Simular condiciones de mercado variadas
            market_conditions = {
                "volatility_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
                "volatility_value": round(random.uniform(0.5, 5.0), 2),
                "trend_strength": random.choice(["WEAK", "STRONG_BULLISH", "STRONG_BEARISH"]),
                "volume_ratio": round(random.uniform(0.5, 2.5), 2),
                "rsi": random.randint(20, 80)
            }
            
            # Ejecutar ciclo
            if self.run_complete_trading_cycle():
                successful_cycles += 1
            
            # Pequeña pausa entre ciclos
            time.sleep(1)
        
        success_rate = (successful_cycles / num_cycles) * 100
        self.log_test(f"Stress Test ({num_cycles} ciclos)", 
                     success_rate >= 80, 
                     f"{successful_cycles}/{num_cycles} ciclos exitosos ({success_rate:.1f}%)")
        
        return success_rate >= 80
    
    def run_all_tests(self):
        """Ejecuta toda la suite de pruebas"""
        print("🚀 Iniciando Suite de Pruebas Automatizadas\n")
        
        # Pruebas básicas
        print("=== PRUEBAS BÁSICAS ===")
        basic_tests = [
            self.test_health_check,
            self.test_paper_trading_reset,
            self.test_get_portfolio,
            self.test_trading_endpoints
        ]
        
        for test in basic_tests:
            test()
            time.sleep(0.5)
        
        # Pruebas de paper trading
        print("\n=== PRUEBAS DE PAPER TRADING ===")
        buy_success, buy_order = self.test_place_buy_order()
        time.sleep(1)
        sell_success, sell_order = self.test_place_sell_order()
        
        # Pruebas de aprendizaje
        print("\n=== PRUEBAS DE APRENDIZAJE ===")
        if buy_success and sell_success:
            self.test_learning_record_trade(buy_order, sell_order)
        
        self.test_learning_evaluation()
        self.test_get_learning_performance()
        
        # Ciclo completo
        print("\n=== PRUEBA DE CICLO COMPLETO ===")
        self.run_complete_trading_cycle()
        
        # Stress test
        print("\n=== STRESS TEST ===")
        self.run_stress_test(3)  # 3 ciclos para prueba rápida
        
        # Resultados finales
        self.print_test_summary()
    
    def print_test_summary(self):
        """Imprime resumen de todas las pruebas"""
        print("\n" + "="*50)
        print("📊 RESUMEN DE PRUEBAS")
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
        
        print("\n🎯 RECOMENDACIONES:")
        if passed_tests / total_tests >= 0.9:
            print("  ✅ Sistema funcionando correctamente")
            print("  ✅ Paper trading operativo")
            print("  ✅ Sistema de aprendizaje activo")
        elif passed_tests / total_tests >= 0.7:
            print("  ⚠️ Sistema parcialmente funcional")
            print("  ⚠️ Revisar pruebas fallidas")
        else:
            print("  ❌ Sistema requiere atención")
            print("  ❌ Revisar configuración y dependencias")


def main():
    """Función principal para ejecutar las pruebas"""
    print("🤖 IA-AGENTS Trading Bot - Suite de Pruebas Automatizadas")
    print("=" * 60)
    
    # Verificar que la API esté corriendo
    test_suite = TradingTestSuite()
    
    try:
        response = requests.get("http://localhost:8000")
        if response.status_code != 200:
            print("❌ Error: API no responde en http://localhost:8000")
            print("   Asegúrate de que el servidor esté corriendo:")
            print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Ejecutar suite de pruebas
    test_suite.run_all_tests()


if __name__ == "__main__":
    main()
