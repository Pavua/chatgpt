# SwiftUI Client

Этот каталог содержит минимальное приложение SwiftUI, которое подключается к HTTP API бота.

## Сборка

```bash
swift build -c release
```

Запуск приложения потребует macOS 12+ или iOS 15+.

### Уведомления и автозапуск

При первом запуске приложение запросит разрешение на отправку уведомлений.
Оно будет показывать уведомление при смене активной модели или стиля.

Чтобы приложение автоматически стартовало после входа в систему,
можно создать LaunchAgent используя пример `launch_agent.plist`:

```bash
mkdir -p ~/Library/LaunchAgents
cp launch_agent.plist ~/Library/LaunchAgents/com.userbot.app.plist
launchctl load ~/Library/LaunchAgents/com.userbot.app.plist
```
