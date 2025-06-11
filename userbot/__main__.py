from .bot import main
from .utils import ensure_dependencies

if __name__ == '__main__':
    import asyncio
    ensure_dependencies()
    asyncio.run(main())
