//
//  DriverView.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import SwiftUI
import MapKit

struct DriverView: View {
    @State private var isOnline = false
    @State private var availableRides: [DriverRide] = []
    @State private var currentRide: DriverRide? = nil
    @State private var cameraPosition = MapCameraPosition.region(
        MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194),
            span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
        )
    )
    
    var body: some View {
        ZStack {
            // Map View
            Map(position: $cameraPosition) {
                UserAnnotation()
            }
            .ignoresSafeArea()
            
            VStack {
                // Top Controls
                HStack {
                    Spacer()
                    VStack(spacing: 8) {
                        // Online/Offline Toggle
                        Button(action: {
                            isOnline.toggle()
                            if isOnline {
                                loadAvailableRides()
                            } else {
                                availableRides = []
                                currentRide = nil
                            }
                        }) {
                            HStack {
                                Circle()
                                    .fill(isOnline ? Color.green : Color.gray)
                                    .frame(width: 12, height: 12)
                                Text(isOnline ? "Online" : "Offline")
                                    .font(.headline)
                                    .foregroundColor(.white)
                            }
                            .padding(.horizontal, 20)
                            .padding(.vertical, 12)
                            .background(isOnline ? Color.green : Color.gray)
                            .cornerRadius(25)
                        }
                        
                        // Earnings Summary
                        if isOnline {
                            VStack(spacing: 4) {
                                Text("Today's Earnings")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                                Text("$0.00")
                                    .font(.title2)
                                    .fontWeight(.bold)
                            }
                            .padding()
                            .background(Color(.systemBackground))
                            .cornerRadius(12)
                            .shadow(radius: 5)
                        }
                    }
                    .padding()
                }
                
                Spacer()
                
                // Bottom Sheet
                if isOnline {
                    VStack(spacing: 0) {
                        // Handle bar
                        RoundedRectangle(cornerRadius: 3)
                            .fill(Color.gray.opacity(0.3))
                            .frame(width: 40, height: 5)
                            .padding(.top, 8)
                        
                        if let ride = currentRide {
                            // Active Ride View
                            DriverActiveRideView(ride: ride)
                        } else if !availableRides.isEmpty {
                            // Available Rides List
                            ScrollView {
                                VStack(spacing: 12) {
                                    Text("Available Rides")
                                        .font(.headline)
                                        .frame(maxWidth: .infinity, alignment: .leading)
                                        .padding(.horizontal)
                                    
                                    ForEach(availableRides) { ride in
                                        RideRequestCard(ride: ride) {
                                            acceptRide(ride)
                                        }
                                    }
                                }
                                .padding(.vertical)
                            }
                        } else {
                            // Waiting for rides
                            VStack(spacing: 16) {
                                Image(systemName: "car.fill")
                                    .font(.system(size: 50))
                                    .foregroundColor(.blue)
                                Text("Waiting for ride requests...")
                                    .font(.headline)
                                    .foregroundColor(.secondary)
                                Text("You'll be notified when a ride is available")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                                    .multilineTextAlignment(.center)
                            }
                            .padding(40)
                        }
                    }
                    .background(Color(.systemBackground))
                    .cornerRadius(20, corners: [.topLeft, .topRight])
                    .shadow(radius: 10)
                    .frame(maxHeight: 400)
                }
            }
        }
    }
    
    private func loadAvailableRides() {
        // Simulate loading available rides
        availableRides = [
            DriverRide(
                pickupLocation: Location(name: "123 Main St", latitude: 37.7750, longitude: -122.4195),
                destinationLocation: Location(name: "456 Market St", latitude: 37.7850, longitude: -122.4095),
                riderName: "Sarah Johnson",
                riderRating: 4.9,
                fare: 18.50,
                status: .matched
            ),
            DriverRide(
                pickupLocation: Location(name: "789 Oak Ave", latitude: 37.7760, longitude: -122.4200),
                destinationLocation: Location(name: "321 Pine St", latitude: 37.7860, longitude: -122.4100),
                riderName: "Mike Chen",
                riderRating: 4.7,
                fare: 22.00,
                status: .matched
            )
        ]
    }
    
    private func acceptRide(_ ride: DriverRide) {
        currentRide = ride
        availableRides.removeAll { $0.id == ride.id }
    }
}

struct RideRequestCard: View {
    let ride: DriverRide
    let onAccept: () -> Void
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(ride.riderName)
                        .font(.headline)
                    HStack(spacing: 4) {
                        Image(systemName: "star.fill")
                            .foregroundColor(.yellow)
                            .font(.caption)
                        Text(String(format: "%.1f", ride.riderRating))
                            .font(.caption)
                    }
                }
                Spacer()
                Text("$\(String(format: "%.2f", ride.fare))")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.green)
            }
            
            Divider()
            
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Circle()
                        .fill(Color.green)
                        .frame(width: 8, height: 8)
                    Text(ride.pickupLocation.name)
                        .font(.subheadline)
                }
                HStack {
                    Circle()
                        .fill(Color.red)
                        .frame(width: 8, height: 8)
                    Text(ride.destinationLocation.name)
                        .font(.subheadline)
                }
            }
            
            Button(action: onAccept) {
                Text("Accept Ride")
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .cornerRadius(12)
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(16)
        .padding(.horizontal)
    }
}

struct DriverActiveRideView: View {
    let ride: DriverRide
    
    var body: some View {
        VStack(spacing: 16) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("Current Ride")
                        .font(.headline)
                    Text(ride.riderName)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                Spacer()
                HStack(spacing: 4) {
                    Image(systemName: "star.fill")
                        .foregroundColor(.yellow)
                    Text(String(format: "%.1f", ride.riderRating))
                        .font(.subheadline)
                }
            }
            
            Divider()
            
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Circle()
                        .fill(Color.green)
                        .frame(width: 12, height: 12)
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Pickup")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        Text(ride.pickupLocation.name)
                            .font(.subheadline)
                    }
                }
                
                HStack {
                    Circle()
                        .fill(Color.red)
                        .frame(width: 12, height: 12)
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Destination")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        Text(ride.destinationLocation.name)
                            .font(.subheadline)
                    }
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            
            HStack {
                Text("Fare:")
                    .foregroundColor(.secondary)
                Spacer()
                Text("$\(String(format: "%.2f", ride.fare))")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.green)
            }
            
            Button(action: {
                // Complete ride action
            }) {
                Text("Complete Ride")
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.green)
                    .cornerRadius(12)
            }
        }
        .padding()
    }
}

#Preview {
    DriverView()
}

