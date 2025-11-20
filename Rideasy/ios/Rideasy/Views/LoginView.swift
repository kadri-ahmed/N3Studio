//
//  LoginView.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import SwiftUI

struct LoginView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var email = ""
    @State private var password = ""
    @State private var showPassword = false
    @FocusState private var focusedField: Field?
    
    enum Field {
        case email, password
    }
    
    var body: some View {
        VStack(spacing: 24) {
            // Logo/Title
            VStack(spacing: 8) {
                Text("Rideasy")
                    .font(.system(size: 48, weight: .bold))
                    .foregroundColor(.blue)
                
                Text("Sign in to continue")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            .padding(.top, 60)
            
            Spacer()
            
            // Form
            VStack(spacing: 20) {
                // Email Field
                VStack(alignment: .leading, spacing: 8) {
                    Text("Email")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    TextField("Enter your email", text: $email)
                        .textFieldStyle(.plain)
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                        .autocorrectionDisabled()
                        .focused($focusedField, equals: .email)
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(12)
                }
                
                // Password Field
                VStack(alignment: .leading, spacing: 8) {
                    Text("Password")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    HStack {
                        if showPassword {
                            TextField("Enter your password", text: $password)
                                .textFieldStyle(.plain)
                        } else {
                            SecureField("Enter your password", text: $password)
                                .textFieldStyle(.plain)
                        }
                        
                        Button(action: {
                            showPassword.toggle()
                        }) {
                            Image(systemName: showPassword ? "eye.slash.fill" : "eye.fill")
                                .foregroundColor(.secondary)
                        }
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                    .focused($focusedField, equals: .password)
                }
                
                // Error Message
                if let errorMessage = authViewModel.errorMessage {
                    Text(errorMessage)
                        .font(.caption)
                        .foregroundColor(.red)
                        .padding(.horizontal)
                }
                
                // Login Button
                Button(action: {
                    Task {
                        await authViewModel.login(email: email, password: password)
                    }
                }) {
                    HStack {
                        if authViewModel.isLoading {
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        } else {
                            Text("Sign In")
                                .fontWeight(.semibold)
                        }
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(
                        email.isEmpty || password.isEmpty || authViewModel.isLoading
                        ? Color.gray
                        : Color.blue
                    )
                    .foregroundColor(.white)
                    .cornerRadius(12)
                }
                .disabled(email.isEmpty || password.isEmpty || authViewModel.isLoading)
            }
            .padding(.horizontal, 24)
            
            Spacer()
        }
        .onSubmit {
            if focusedField == .email {
                focusedField = .password
            } else {
                Task {
                    await authViewModel.login(email: email, password: password)
                }
            }
        }
    }
}

#Preview {
    LoginView()
        .environmentObject(AuthViewModel())
}

