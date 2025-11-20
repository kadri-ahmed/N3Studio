//
//  MainView.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import SwiftUI

struct MainView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var selectedMode: UserMode = .rider
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Mode Selector
                Picker("Mode", selection: $selectedMode) {
                    Text("Rider").tag(UserMode.rider)
                    Text("Driver").tag(UserMode.driver)
                }
                .pickerStyle(.segmented)
                .padding()
                
                // Content based on selected mode
                if selectedMode == .rider {
                    RiderView()
                } else {
                    DriverView()
                }
            }
            .navigationTitle("Rideasy")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Menu {
                        if let user = authViewModel.currentUser {
                            Text("Signed in as \(user.username)")
                                .font(.caption)
                        }
                        Button(action: {
                            authViewModel.logout()
                        }) {
                            Label("Sign Out", systemImage: "arrow.right.square")
                        }
                    } label: {
                        Image(systemName: "person.circle")
                    }
                }
            }
        }
    }
}

#Preview {
    MainView()
}

