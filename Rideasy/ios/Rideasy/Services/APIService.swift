//
//  APIService.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import Foundation

class APIService {
    static let shared = APIService()
    
    private let baseURL = APIConfig.baseURL
    
    private init() {}
    
    func request<T: Decodable>(
        endpoint: String,
        method: String = "GET",
        body: Encodable? = nil,
        token: String? = nil
    ) async throws -> T {
        guard let url = URL(string: "\(baseURL)\(endpoint)") else {
            throw APIError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let token = token {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        
        if let body = body {
            do {
                request.httpBody = try JSONEncoder().encode(body)
            } catch {
                throw APIError.encodingError
            }
        }
        
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                throw APIError.invalidResponse
            }
            
            guard (200...299).contains(httpResponse.statusCode) else {
                if let errorData = try? JSONDecoder().decode(APIErrorResponse.self, from: data) {
                    throw APIError.serverError(errorData.detail)
                }
                throw APIError.httpError(httpResponse.statusCode)
            }
            
            do {
                let decoder = JSONDecoder()
                
                // Configure date decoding with multiple format support
                decoder.dateDecodingStrategy = .custom { decoder in
                    let container = try decoder.singleValueContainer()
                    let dateString = try container.decode(String.self)
                    
                    // Try ISO8601 with fractional seconds
                    let formatter1 = ISO8601DateFormatter()
                    formatter1.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
                    if let date = formatter1.date(from: dateString) {
                        return date
                    }
                    
                    // Try standard ISO8601
                    let formatter2 = ISO8601DateFormatter()
                    formatter2.formatOptions = [.withInternetDateTime]
                    if let date = formatter2.date(from: dateString) {
                        return date
                    }
                    
                    // Try custom date formats
                    let dateFormatter = DateFormatter()
                    dateFormatter.locale = Locale(identifier: "en_US_POSIX")
                    dateFormatter.timeZone = TimeZone(secondsFromGMT: 0)
                    
                    let formats = [
                        "yyyy-MM-dd'T'HH:mm:ss.SSSSSS",
                        "yyyy-MM-dd'T'HH:mm:ss.SSS",
                        "yyyy-MM-dd'T'HH:mm:ss",
                        "yyyy-MM-dd HH:mm:ss"
                    ]
                    
                    for format in formats {
                        dateFormatter.dateFormat = format
                        if let date = dateFormatter.date(from: dateString) {
                            return date
                        }
                    }
                    
                    throw DecodingError.dataCorruptedError(
                        in: container,
                        debugDescription: "Cannot decode date string \(dateString)"
                    )
                }
                return try decoder.decode(T.self, from: data)
            } catch let decodingError as DecodingError {
                print("=== Decoding Error Details ===")
                switch decodingError {
                case .typeMismatch(let type, let context):
                    print("Type mismatch: Expected \(type), at path: \(context.codingPath.map { $0.stringValue }.joined(separator: "."))")
                    print("Context: \(context.debugDescription)")
                case .valueNotFound(let type, let context):
                    print("Value not found: \(type), at path: \(context.codingPath.map { $0.stringValue }.joined(separator: "."))")
                case .keyNotFound(let key, let context):
                    print("Key not found: \(key.stringValue), at path: \(context.codingPath.map { $0.stringValue }.joined(separator: "."))")
                case .dataCorrupted(let context):
                    print("Data corrupted at path: \(context.codingPath.map { $0.stringValue }.joined(separator: "."))")
                    print("Context: \(context.debugDescription)")
                @unknown default:
                    print("Unknown decoding error: \(decodingError)")
                }
                if let dataString = String(data: data, encoding: .utf8) {
                    print("Response JSON: \(dataString)")
                }
                throw APIError.decodingError
            } catch {
                print("Decoding error: \(error)")
                if let dataString = String(data: data, encoding: .utf8) {
                    print("Response data: \(dataString)")
                }
                throw APIError.decodingError
            }
        } catch let error as APIError {
            throw error
        } catch {
            throw APIError.networkError(error.localizedDescription)
        }
    }
}

enum APIError: LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(Int)
    case serverError(String)
    case encodingError
    case decodingError
    case networkError(String)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .httpError(let code):
            return "HTTP error with code: \(code)"
        case .serverError(let message):
            return message
        case .encodingError:
            return "Failed to encode request"
        case .decodingError:
            return "Failed to decode response"
        case .networkError(let message):
            return "Network error: \(message)"
        }
    }
}

struct APIErrorResponse: Codable {
    let detail: String
}

