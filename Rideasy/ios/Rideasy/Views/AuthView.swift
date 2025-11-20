//
//  AuthView.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import SwiftUI

struct AuthView: View {
    @State private var showingLogin = true
    
    var body: some View {
        VStack(spacing: 0) {
            if showingLogin {
                LoginView()
                    .transition(.move(edge: .leading))
            } else {
                RegisterView()
                    .transition(.move(edge: .trailing))
            }
            
            // Toggle between Login and Register
            HStack {
                Text(showingLogin ? "Don't have an account?" : "Already have an account?")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                
                Button(action: {
                    withAnimation {
                        showingLogin.toggle()
                    }
                }) {
                    Text(showingLogin ? "Sign Up" : "Sign In")
                        .font(.subheadline)
                        .fontWeight(.semibold)
                        .foregroundColor(.blue)
                }
            }
            .padding(.bottom, 40)
        }
    }
}

#Preview {
    AuthView()
        .environmentObject(AuthViewModel())
}

