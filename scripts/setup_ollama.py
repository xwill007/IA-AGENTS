#!/usr/bin/env python3
"""
IA-AGENTS: Ollama Management Script
Configura y gestiona modelos de IA a través de Docker
"""

import requests
import json
import time
import logging
import sys
import os
from typing import Dict, Any, Optional

# Configuración - Detectar si estamos en Docker
if os.path.exists('/.dockerenv'):
    # Dentro del contenedor Docker
    OLLAMA_BASE_URL = "http://ollama:11434"
else:
    # Host local
    OLLAMA_BASE_URL = "http://localhost:11434"
REQUIRED_MODEL = "llama3.1:8b"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaManager:
    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url
        
    def health_check(self) -> bool:
        """Verifica si Ollama está respondiendo"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def list_models(self) -> list:
        """Lista modelos disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get('models', [])
            return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def model_exists(self, model_name: str) -> bool:
        """Verifica si un modelo específico existe"""
        models = self.list_models()
        return any(model.get('name', '').startswith(model_name) for model in models)
    
    def pull_model(self, model_name: str) -> bool:
        """Descarga un modelo"""
        try:
            logger.info(f"Iniciando descarga de modelo: {model_name}")
            
            payload = {"name": model_name}
            response = requests.post(
                f"{self.base_url}/api/pull",
                json=payload,
                stream=True,
                timeout=3600  # 1 hora timeout
            )
            
            if response.status_code != 200:
                logger.error(f"Error en descarga: {response.status_code}")
                return False
            
            # Procesar respuesta de streaming
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'status' in data:
                            logger.info(f"Estado: {data['status']}")
                        if data.get('status') == 'success':
                            logger.info(f"Modelo {model_name} descargado exitosamente")
                            return True
                    except json.JSONDecodeError:
                        continue
            
            return True
            
        except Exception as e:
            logger.error(f"Error descargando modelo: {e}")
            return False
    
    def test_model(self, model_name: str) -> Optional[str]:
        """Prueba un modelo con un prompt simple"""
        try:
            payload = {
                "model": model_name,
                "prompt": "Hello! I'm ready to analyze cryptocurrency trading data. Please provide market information.",
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logger.error(f"Error testing model: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error testing model: {e}")
            return None
    
    def setup_ia_agents_model(self) -> Dict[str, Any]:
        """Configura el modelo principal para IA-AGENTS"""
        result = {
            "success": False,
            "model": REQUIRED_MODEL,
            "status": "",
            "response": None
        }
        
        # 1. Health check
        if not self.health_check():
            result["status"] = "Ollama no está disponible"
            return result
        
        logger.info("✅ Ollama está respondiendo")
        
        # 2. Verificar si el modelo existe
        if self.model_exists(REQUIRED_MODEL):
            logger.info(f"✅ Modelo {REQUIRED_MODEL} ya está disponible")
            result["status"] = "Model already available"
        else:
            # 3. Descargar modelo
            logger.info(f"⬇️ Descargando modelo {REQUIRED_MODEL}...")
            if not self.pull_model(REQUIRED_MODEL):
                result["status"] = "Error downloading model"
                return result
            
            logger.info(f"✅ Modelo {REQUIRED_MODEL} descargado")
            result["status"] = "Model downloaded successfully"
        
        # 4. Probar modelo
        logger.info("🧪 Probando modelo...")
        test_response = self.test_model(REQUIRED_MODEL)
        
        if test_response:
            logger.info("✅ Modelo probado exitosamente")
            result["success"] = True
            result["response"] = test_response
            result["status"] += " and tested successfully"
        else:
            result["status"] += " but testing failed"
        
        return result

def main():
    """Función principal"""
    print("🤖 IA-AGENTS: Configurando Ollama...")
    
    manager = OllamaManager()
    result = manager.setup_ia_agents_model()
    
    print("\n" + "="*50)
    print("📊 RESULTADO DE CONFIGURACIÓN")
    print("="*50)
    print(f"Modelo: {result['model']}")
    print(f"Estado: {result['status']}")
    print(f"Éxito: {'✅' if result['success'] else '❌'}")
    
    if result['response']:
        print(f"\n🧠 Respuesta del modelo:")
        print(f"'{result['response'][:200]}{'...' if len(result['response']) > 200 else ''}'")
    
    print("\n" + "="*50)
    
    if result['success']:
        print("🎉 ¡Ollama configurado exitosamente para IA-AGENTS!")
        print("\n📝 Próximos pasos:")
        print("1. Configurar workflows en n8n")
        print("2. Probar análisis de trading")
        print("3. Configurar automatización")
    else:
        print("❌ Error en configuración. Revisar logs.")
    
    return result

if __name__ == "__main__":
    main()
