import asyncio
import signal
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from utils.logger import get_logger
from core.trading_engine import TradingEngine
from api.health_check import start_health_server

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan():
    # Startup
    load_dotenv()
    logger.info("Starting Cryptobot")
    
    # Start health check server
    health_server = await start_health_server()
    
    # Handle shutdown
    def shutdown_handler():
        logger.warning("Shutdown signal received")
        health_server.close()
    
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)
    
    try:
        yield
    finally:
        # Cleanup
        logger.info("Shutting down Cryptobot")

async def main():
    async with lifespan():
        engine = TradingEngine()
        try:
            await engine.run()
        except Exception as e:
            logger.critical(f"Fatal error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())