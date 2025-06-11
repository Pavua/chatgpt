import SwiftUI

struct Status: Decodable {
    var model: String
    var style: String
    var temperature: Double
}

struct ContentView: View {
    @State private var status = Status(model: "-", style: "-", temperature: 0.0)
    @State private var lastStatus = Status(model: "-", style: "-", temperature: 0.0)
    @State private var models: [String] = []
    @State private var styles: [String] = []
    @State private var message = ""

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Picker("Model", selection: $status.model) {
                    ForEach(models, id: \.self) { Text($0) }
                }
                .onChange(of: status.model) { m in switchModel(m) }

                Picker("Style", selection: $status.style) {
                    ForEach(styles, id: \.self) { Text($0) }
                }
                .onChange(of: status.style) { s in switchStyle(s) }
            }
            Text("Temp: \(status.temperature, specifier: "%.2f")")
            Button("Reload") { fetchStatus() }
            Divider()
            ScrollView {
                Text(message).frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .padding()
        .task {
            await fetchOptions()
            await fetchStatus()
        }
        .frame(minWidth: 300, minHeight: 200)
    }

    func fetchStatus() async {
        guard let url = URL(string: "http://127.0.0.1:8080/status") else { return }
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            if let s = try? JSONDecoder().decode(Status.self, from: data) {
                await MainActor.run {
                    if s.model != lastStatus.model || s.style != lastStatus.style {
                        NotificationManager.shared.send(title: "Userbot", body: "Model: \(s.model), Style: \(s.style)")
                    }
                    status = s
                    lastStatus = s
                }
            }
        } catch {
            await MainActor.run { message = "Ошибка запроса: \(error)" }
        }
    }

    func fetchOptions() async {
        guard let url = URL(string: "http://127.0.0.1:8080/options") else { return }
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            if let opts = try? JSONSerialization.jsonObject(with: data) as? [String: [String]] {
                await MainActor.run {
                    models = opts["models"] ?? []
                    styles = opts["styles"] ?? []
                }
            }
        } catch {}
    }

    func switchModel(_ m: String) {
        guard let url = URL(string: "http://127.0.0.1:8080/model") else { return }
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.httpBody = m.data(using: .utf8)
        req.setValue("text/plain", forHTTPHeaderField: "Content-Type")
        URLSession.shared.dataTask(with: req).resume()
    }

    func switchStyle(_ s: String) {
        guard let url = URL(string: "http://127.0.0.1:8080/style") else { return }
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.httpBody = s.data(using: .utf8)
        req.setValue("text/plain", forHTTPHeaderField: "Content-Type")
        URLSession.shared.dataTask(with: req).resume()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

