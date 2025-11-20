//
//  AuthService.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import Foundation

class AuthService {
    static let shared = AuthService()
    
    private let apiService = APIService.shared
    private let tokenKey = "auth_token"
    private let userKey = "current_user"
    
    private init() {}
    
    // MARK: - Authentication
    
    func register(_ request: RegisterRequest) async throws -> AuthResponse {
        return try await apiService.request(
            endpoint: "/auth/register",
            method: "POST",
            body: request
        )
    }
    
    func login(_ request: LoginRequest) async throws -> AuthResponse {
        return try await apiService.request(
            endpoint: "/auth/login",
            method: "POST",
            body: request
        )
    }
    
    func getCurrentUser(token: String) async throws -> User {
        return try await apiService.request(
            endpoint: "/auth/me",
            method: "GET",
            token: token
        )
    }
    
    // MARK: - Token Management
    
    func saveToken(_ token: String) {
        UserDefaults.standard.set(token, forKey: tokenKey)
    }
    
    func getToken() -> String? {
        return UserDefaults.standard.string(forKey: tokenKey)
    }
    
    func removeToken() {
        UserDefaults.standard.removeObject(forKey: tokenKey)
        UserDefaults.standard.removeObject(forKey: userKey)
    }
    
    // MARK: - User Management
    
    func saveUser(_ user: User) {
        if let encoded = try? JSONEncoder().encode(user) {
            UserDefaults.standard.set(encoded, forKey: userKey)
        }
    }
    
    func getCurrentUser() -> User? {
        guard let data = UserDefaults.standard.data(forKey: userKey),
              let user = try? JSONDecoder().decode(User.self, from: data) else {
            return nil
        }
        return user
    }
    
    func isAuthenticated() -> Bool {
        return getToken() != nil
    }
}

