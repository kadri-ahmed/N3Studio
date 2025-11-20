//
//  AuthViewModel.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import Foundation
import SwiftUI
import Combine

class AuthViewModel: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let authService = AuthService.shared
    
    init() {
        checkAuthentication()
    }
    
    func checkAuthentication() {
        if authService.isAuthenticated(), let user = authService.getCurrentUser() {
            DispatchQueue.main.async {
                self.isAuthenticated = true
                self.currentUser = user
            }
        }
    }
    
    @MainActor
    func login(email: String, password: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let request = LoginRequest(email: email, password: password)
            let response = try await authService.login(request)
            
            authService.saveToken(response.accessToken)
            authService.saveUser(response.user)
            
            self.currentUser = response.user
            self.isAuthenticated = true
        } catch {
            if let apiError = error as? APIError {
                errorMessage = apiError.errorDescription
            } else {
                errorMessage = "Login failed: \(error.localizedDescription)"
            }
        }
        
        isLoading = false
    }
    
    @MainActor
    func register(
        email: String,
        username: String,
        password: String,
        fullName: String? = nil,
        phoneNumber: String? = nil,
        userMode: UserMode = .rider
    ) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let request = RegisterRequest(
                email: email,
                username: username,
                password: password,
                fullName: fullName,
                phoneNumber: phoneNumber,
                userMode: userMode
            )
            let response = try await authService.register(request)
            
            authService.saveToken(response.accessToken)
            authService.saveUser(response.user)
            
            self.currentUser = response.user
            self.isAuthenticated = true
        } catch {
            if let apiError = error as? APIError {
                errorMessage = apiError.errorDescription
            } else {
                errorMessage = "Registration failed: \(error.localizedDescription)"
            }
        }
        
        isLoading = false
    }
    
    @MainActor
    func logout() {
        authService.removeToken()
        self.isAuthenticated = false
        self.currentUser = nil
    }
}

