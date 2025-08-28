# 🔐 Seguridad - IA-AGENTS
## Mejores Prácticas de Seguridad

---

## ⚠️ IMPORTANTE - Gestión de Credenciales

### ✅ Lo que SÍ debes hacer:

1. **Copiar env.example a .env:**
   ```bash
   cp env.example .env
   ```

2. **Editar .env con TUS credenciales:**
   ```bash
   # Usar tu editor preferido
   nano .env
   # o
   code .env
   ```

3. **Configurar credenciales REALES en .env:**
   ```bash
   BINANCE_API_KEY=tu_api_key_real_aqui
   BINANCE_API_SECRET=tu_api_secret_real_aqui
   N8N_BASIC_AUTH_PASSWORD=tu_password_seguro
   ```

### ❌ Lo que NO debes hacer:

1. **NUNCA subir .env al repositorio**
   - El archivo .env está en .gitignore
   - Contiene credenciales sensibles
   - Solo debe existir localmente

2. **NUNCA poner credenciales reales en env.example**
   - env.example solo tiene placeholders
   - Se sube al repositorio público
   - Solo ejemplos seguros

3. **NUNCA compartir credenciales en documentación**
   - Documentación pública
   - Riesgo de exposición
   - Usar solo ejemplos

---

## 🔒 Configuración de Seguridad Actual

### Archivos Protegidos (.gitignore):
```
.env
.env.local
.env.production
.env.staging
data/
models/
logs/
notebooks/
```

### Variables Sensibles:
- `BINANCE_API_KEY` - API key de Binance
- `BINANCE_API_SECRET` - Secret de Binance
- `N8N_BASIC_AUTH_PASSWORD` - Contraseña de n8n
- `JUPYTER_TOKEN` - Token de Jupyter
- `GF_SECURITY_ADMIN_PASSWORD` - Contraseña de Grafana

---

## 🛡️ Configuración Segura por Defecto

### Trading:
- ✅ `BINANCE_TESTNET=true` - Solo testnet
- ✅ `TRADING_ENABLED=false` - Paper trading
- ✅ Balance virtual inicial: $10,000 USD

### Acceso:
- 🔐 n8n protegido con autenticación básica
- 🔐 Grafana con contraseña de admin
- 🔐 Jupyter con token de acceso
- 🌐 APIs solo en localhost por defecto

---

## 🚀 Para Producción (Futuro)

### Cuando estés listo para trading real:
```bash
# ⚠️ SOLO cuando hayas probado exhaustivamente
BINANCE_TESTNET=false
TRADING_ENABLED=true
```

### Configuración adicional para producción:
- [ ] SSL/TLS certificates
- [ ] Reverse proxy (nginx)
- [ ] Firewall configuration
- [ ] Backup automatizado
- [ ] Monitoring de seguridad
- [ ] Rate limiting
- [ ] IP whitelisting

---

## 📞 En Caso de Problemas

### Si crees que tus credenciales fueron expuestas:
1. **Inmediatamente:** Regenerar API keys en Binance
2. **Cambiar:** Todas las contraseñas de servicios
3. **Revisar:** Logs de acceso
4. **Verificar:** Que .env no se subió al repositorio

### Para verificar seguridad:
```bash
# Verificar que .env está en .gitignore
cat .gitignore | grep .env

# Verificar que .env no está trackeado por git
git status --ignored

# Verificar configuración actual
docker-compose ps
```

---

## ✅ Checklist de Seguridad

- [ ] .env copiado de env.example
- [ ] Credenciales reales configuradas en .env
- [ ] .env en .gitignore
- [ ] env.example sin credenciales reales
- [ ] Contraseñas de servicios cambiadas
- [ ] Testnet habilitado
- [ ] Trading real deshabilitado
- [ ] Documentación sin credenciales

**¡Mantén tu sistema seguro!** 🔐
