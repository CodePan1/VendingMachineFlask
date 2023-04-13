from ..models import StockTimeline


def get_product_stock_timeline(product_id):
    return StockTimeline.query.filter_by(product_id=product_id).order_by(StockTimeline.timestamp).all()


def get_vending_machine_stock_timeline(vending_machine_id):
    return StockTimeline.query.filter_by(vending_machine_id=vending_machine_id).order_by(StockTimeline.timestamp).all()
