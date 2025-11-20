//
//  RideasyApp.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import SwiftUI

@main
struct RideasyApp: App {
    @StateObject private var authViewModel = AuthViewModel()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authViewModel)
        }
    }
}
