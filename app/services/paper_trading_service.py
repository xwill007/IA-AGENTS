"""
Paper Trading Engine para simulación de operaciones sin dinero real
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import uuid
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class OrderStatus(Enum):
    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass
class PaperOrder:
    id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    order_type: str  # MARKET, LIMIT
    status: OrderStatus
    created_at: datetime
    filled_at: Optional[datetime] = None
    filled_price: Optional[float] = None
    filled_quantity: Optional[float] = None

@dataclass
class PaperPosition:
    symbol: str
    quantity: float
    avg_entry_price: float
    unrealized_pnl: float
    realized_pnl: float
    created_at: datetime

class PaperTradingEngine:
    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.positions: Dict[str, PaperPosition] = {}
        self.orders: List[PaperOrder] = []
        self.trade_history: List[Dict] = []
        self.current_prices: Dict[str, float] = {}
        self.transaction_fee = 0.001  # 0.1% fee
    
    def update_market_price(self, symbol: str, price: float):
        """Actualiza precio de mercado para un símbolo"""
        self.current_prices[symbol] = price
        self._update_unrealized_pnl(symbol)
    
    def place_order(self, symbol: str, side: OrderSide, quantity: float, 
                   order_type: str = "MARKET", price: Optional[float] = None) -> Dict:
        """Coloca una orden de paper trading"""
        
        # Validaciones básicas
        if order_type == "MARKET":
            if symbol not in self.current_prices:
                return {"error": "No hay precio de mercado disponible"}
            execution_price = self.current_prices[symbol]
        else:
            execution_price = price
        
        # Agregar slippage realista para órdenes de mercado
        if order_type == "MARKET":
            slippage = 0.0005  # 0.05% slippage
            if side == OrderSide.BUY:
                execution_price *= (1 + slippage)
            else:
                execution_price *= (1 - slippage)
        
        # Crear orden
        order = PaperOrder(
            id=str(uuid.uuid4()),
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=execution_price,
            order_type=order_type,
            status=OrderStatus.PENDING,
            created_at=datetime.now()
        )
        
        # Ejecutar inmediatamente para MARKET orders
        if order_type == "MARKET":
            return self._execute_order(order)
        
        self.orders.append(order)
        return {"order_id": order.id, "status": "PENDING"}
    
    def _execute_order(self, order: PaperOrder) -> Dict:
        """Ejecuta una orden de paper trading"""
        
        # Calcular costos de transacción
        transaction_cost = order.quantity * order.price * self.transaction_fee
        
        # Verificar saldo disponible para compras
        if order.side == OrderSide.BUY:
            required_balance = (order.quantity * order.price) + transaction_cost
            if required_balance > self.current_balance:
                order.status = OrderStatus.REJECTED
                return {"error": "Saldo insuficiente", "order_id": order.id}
        
        # Verificar posición disponible para ventas
        elif order.side == OrderSide.SELL:
            position = self.positions.get(order.symbol)
            if not position or position.quantity < order.quantity:
                order.status = OrderStatus.REJECTED
                return {"error": "Posición insuficiente", "order_id": order.id}
        
        # Ejecutar orden
        order.status = OrderStatus.FILLED
        order.filled_at = datetime.now()
        order.filled_price = order.price
        order.filled_quantity = order.quantity
        
        # Actualizar posiciones y balance
        self._update_position(order, transaction_cost)
        
        # Registrar trade
        trade_record = {
            "id": order.id,
            "symbol": order.symbol,
            "side": order.side.value,
            "quantity": order.quantity,
            "price": order.price,
            "transaction_cost": transaction_cost,
            "timestamp": order.filled_at,
            "balance_after": self.current_balance
        }
        self.trade_history.append(trade_record)
        
        logger.info(f"✅ Paper Trade: {order.side.value} {order.quantity:.6f} {order.symbol} @ {order.price:.4f}")
        
        return {
            "order_id": order.id,
            "status": "FILLED",
            "filled_price": order.price,
            "filled_quantity": order.quantity,
            "transaction_cost": transaction_cost
        }
    
    def _update_position(self, order: PaperOrder, transaction_cost: float):
        """Actualiza posiciones después de ejecutar orden"""
        symbol = order.symbol
        
        if order.side == OrderSide.BUY:
            # Compra: agregar a posición o crear nueva
            if symbol in self.positions:
                pos = self.positions[symbol]
                total_cost = (pos.quantity * pos.avg_entry_price) + (order.quantity * order.price)
                total_quantity = pos.quantity + order.quantity
                pos.avg_entry_price = total_cost / total_quantity
                pos.quantity = total_quantity
            else:
                self.positions[symbol] = PaperPosition(
                    symbol=symbol,
                    quantity=order.quantity,
                    avg_entry_price=order.price,
                    unrealized_pnl=0.0,
                    realized_pnl=0.0,
                    created_at=datetime.now()
                )
            
            # Reducir balance (incluir costos de transacción)
            self.current_balance -= (order.quantity * order.price) + transaction_cost
        
        else:  # SELL
            # Venta: reducir posición
            pos = self.positions[symbol]
            
            # Calcular PnL realizado
            realized_pnl = (order.price - pos.avg_entry_price) * order.quantity
            pos.realized_pnl += realized_pnl
            
            # Actualizar posición
            pos.quantity -= order.quantity
            
            # Aumentar balance (menos costos de transacción)
            self.current_balance += (order.quantity * order.price) - transaction_cost
            
            # Eliminar posición si está cerrada
            if pos.quantity <= 0:
                del self.positions[symbol]
    
    def _update_unrealized_pnl(self, symbol: str):
        """Actualiza PnL no realizado para un símbolo"""
        if symbol in self.positions:
            pos = self.positions[symbol]
            current_price = self.current_prices[symbol]
            pos.unrealized_pnl = (current_price - pos.avg_entry_price) * pos.quantity
    
    def close_position(self, symbol: str) -> Dict:
        """Cierra completamente una posición"""
        if symbol not in self.positions:
            return {"error": f"No hay posición abierta para {symbol}"}
        
        position = self.positions[symbol]
        return self.place_order(
            symbol=symbol,
            side=OrderSide.SELL,
            quantity=position.quantity,
            order_type="MARKET"
        )
    
    def get_portfolio_summary(self) -> Dict:
        """Obtiene resumen del portfolio"""
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions.values())
        total_realized_pnl = sum(pos.realized_pnl for pos in self.positions.values())
        
        # Calcular valor total del portfolio
        positions_value = sum(
            pos.quantity * self.current_prices.get(pos.symbol, pos.avg_entry_price) 
            for pos in self.positions.values()
        )
        total_value = self.current_balance + positions_value
        
        # Calcular retorno total
        total_return = ((total_value - self.initial_balance) / self.initial_balance) * 100
        
        return {
            "initial_balance": self.initial_balance,
            "current_balance": self.current_balance,
            "positions_value": positions_value,
            "total_value": total_value,
            "total_pnl": total_value - self.initial_balance,
            "total_return_percentage": total_return,
            "unrealized_pnl": total_unrealized_pnl,
            "realized_pnl": total_realized_pnl,
            "num_positions": len(self.positions),
            "num_trades": len(self.trade_history),
            "positions": [
                {
                    "symbol": pos.symbol,
                    "quantity": pos.quantity,
                    "avg_entry_price": pos.avg_entry_price,
                    "current_price": self.current_prices.get(pos.symbol, 0),
                    "market_value": pos.quantity * self.current_prices.get(pos.symbol, pos.avg_entry_price),
                    "unrealized_pnl": pos.unrealized_pnl,
                    "unrealized_pnl_percentage": (pos.unrealized_pnl / (pos.avg_entry_price * pos.quantity)) * 100,
                    "realized_pnl": pos.realized_pnl
                }
                for pos in self.positions.values()
            ]
        }
    
    def get_trade_statistics(self) -> Dict:
        """Obtiene estadísticas de trading"""
        if not self.trade_history:
            return {"message": "No hay trades registrados"}
        
        # Separar compras y ventas
        buys = [t for t in self.trade_history if t["side"] == "BUY"]
        sells = [t for t in self.trade_history if t["side"] == "SELL"]
        
        # Calcular estadísticas básicas
        total_trades = len(self.trade_history)
        total_fees = sum(t.get("transaction_cost", 0) for t in self.trade_history)
        
        # Calcular trades cerrados (simplificado)
        winning_trades = 0
        losing_trades = 0
        total_profit = 0
        total_loss = 0
        
        for pos in self.positions.values():
            if pos.realized_pnl > 0:
                winning_trades += 1
                total_profit += pos.realized_pnl
            elif pos.realized_pnl < 0:
                losing_trades += 1
                total_loss += abs(pos.realized_pnl)
        
        win_rate = (winning_trades / (winning_trades + losing_trades)) * 100 if (winning_trades + losing_trades) > 0 else 0
        
        return {
            "total_trades": total_trades,
            "total_fees": total_fees,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "total_profit": total_profit,
            "total_loss": total_loss,
            "profit_factor": total_profit / total_loss if total_loss > 0 else float('inf'),
            "avg_win": total_profit / winning_trades if winning_trades > 0 else 0,
            "avg_loss": total_loss / losing_trades if losing_trades > 0 else 0
        }
    
    def reset_portfolio(self, new_balance: float = 10000.0):
        """Resetea el portfolio a estado inicial"""
        self.initial_balance = new_balance
        self.current_balance = new_balance
        self.positions.clear()
        self.orders.clear()
        self.trade_history.clear()
        self.current_prices.clear()
        
        logger.info(f"🔄 Portfolio reseteado con balance: ${new_balance:,.2f}")

# Instancia global del paper trading engine
paper_engine = PaperTradingEngine()
