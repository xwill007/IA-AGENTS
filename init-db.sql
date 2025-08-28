-- Inicialización de base de datos para IA-AGENTS Trading Bot
-- Este script se ejecuta automáticamente cuando se crea el contenedor PostgreSQL

-- Crear database para n8n si no existe
SELECT 'CREATE DATABASE n8n'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'n8n')\gexec

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Tablas para el sistema de trading
CREATE TABLE IF NOT EXISTS trading_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    symbol VARCHAR(20) NOT NULL,
    action VARCHAR(50) NOT NULL,
    price DECIMAL(18, 8),
    quantity DECIMAL(18, 8),
    status VARCHAR(20),
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tablas para paper trading
CREATE TABLE IF NOT EXISTS paper_trades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    quantity DECIMAL(18, 8) NOT NULL,
    entry_price DECIMAL(18, 8) NOT NULL,
    exit_price DECIMAL(18, 8),
    pnl DECIMAL(18, 8),
    pnl_percentage DECIMAL(8, 4),
    status VARCHAR(20) DEFAULT 'OPEN',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    closed_at TIMESTAMP WITH TIME ZONE
);

-- Tablas para learning agent
CREATE TABLE IF NOT EXISTS learning_trades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trade_id VARCHAR(100) UNIQUE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    entry_price DECIMAL(18, 8) NOT NULL,
    exit_price DECIMAL(18, 8) NOT NULL,
    quantity DECIMAL(18, 8) NOT NULL,
    pnl DECIMAL(18, 8) NOT NULL,
    pnl_percentage DECIMAL(8, 4) NOT NULL,
    hold_time_minutes INTEGER NOT NULL,
    market_conditions JSONB,
    decision_confidence DECIMAL(4, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tablas para métricas de performance
CREATE TABLE IF NOT EXISTS learning_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    total_trades INTEGER NOT NULL,
    win_rate DECIMAL(5, 4) NOT NULL,
    avg_pnl DECIMAL(18, 8) NOT NULL,
    avg_win DECIMAL(18, 8),
    avg_loss DECIMAL(18, 8),
    sharpe_ratio DECIMAL(8, 4),
    max_drawdown DECIMAL(18, 8),
    profit_factor DECIMAL(8, 4),
    confidence_threshold DECIMAL(4, 3),
    market_weights JSONB,
    optimal_conditions JSONB
);

-- Tablas para configuración del sistema
CREATE TABLE IF NOT EXISTS system_config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insertar configuraciones por defecto
INSERT INTO system_config (key, value, description) VALUES
('paper_trading_balance', '10000.0', 'Balance inicial para paper trading'),
('learning_threshold', '0.6', 'Threshold de confianza para learning agent'),
('transaction_fee', '0.001', 'Fee por transacción (0.1%)'),
('system_version', '1.0.0', 'Versión del sistema'),
('last_learning_update', NOW()::text, 'Última actualización del learning agent')
ON CONFLICT (key) DO NOTHING;

-- Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_trading_logs_timestamp ON trading_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_trading_logs_symbol ON trading_logs(symbol);
CREATE INDEX IF NOT EXISTS idx_paper_trades_symbol ON paper_trades(symbol);
CREATE INDEX IF NOT EXISTS idx_paper_trades_created_at ON paper_trades(created_at);
CREATE INDEX IF NOT EXISTS idx_learning_trades_symbol ON learning_trades(symbol);
CREATE INDEX IF NOT EXISTS idx_learning_trades_created_at ON learning_trades(created_at);
CREATE INDEX IF NOT EXISTS idx_learning_metrics_timestamp ON learning_metrics(timestamp);

-- Crear vistas útiles
CREATE OR REPLACE VIEW portfolio_summary AS
SELECT 
    symbol,
    COUNT(*) as total_trades,
    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as winning_trades,
    SUM(pnl) as total_pnl,
    AVG(pnl) as avg_pnl,
    AVG(pnl_percentage) as avg_pnl_percentage,
    MAX(pnl) as best_trade,
    MIN(pnl) as worst_trade
FROM learning_trades
GROUP BY symbol;

CREATE OR REPLACE VIEW daily_performance AS
SELECT 
    DATE(created_at) as trade_date,
    COUNT(*) as total_trades,
    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as winning_trades,
    SUM(pnl) as daily_pnl,
    AVG(decision_confidence) as avg_confidence
FROM learning_trades
GROUP BY DATE(created_at)
ORDER BY trade_date DESC;

-- Función para limpiar datos antiguos (opcional)
CREATE OR REPLACE FUNCTION cleanup_old_data()
RETURNS void AS $$
BEGIN
    -- Eliminar logs de trading mayores a 30 días
    DELETE FROM trading_logs WHERE created_at < NOW() - INTERVAL '30 days';
    
    -- Eliminar métricas de learning mayores a 90 días
    DELETE FROM learning_metrics WHERE timestamp < NOW() - INTERVAL '90 days';
    
    RAISE NOTICE 'Cleanup completed';
END;
$$ LANGUAGE plpgsql;

COMMIT;
