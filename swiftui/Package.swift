// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "UserbotApp",
    platforms: [
        .macOS(.v12), .iOS(.v15)
    ],
    products: [
        .executable(name: "UserbotApp", targets: ["UserbotApp"])
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "UserbotApp",
            path: "Sources/UserbotApp")
    ]
)
