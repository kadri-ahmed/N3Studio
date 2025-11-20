//
//  RiderView.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import SwiftUI
import MapKit

struct RiderView: View {
    @State private var pickupLocation: String = ""
    @State private var destinationLocation: String = ""
    @State private var currentRide: Ride? = nil
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
                Spacer()
                
                // Bottom Sheet
                VStack(spacing: 20) {
                    // Handle bar
                    RoundedRectangle(cornerRadius: 3)
                        .fill(Color.gray.opacity(0.3))
                        .frame(width: 40, height: 5)
                        .padding(.top, 8)
                    
                    if let ride = currentRide {
                        // Active Ride View
                        ActiveRideView(ride: ride)
                    } else {
                        // Ride Request View
                        VStack(spacing: 16) {
                            // Location Input Fields
                            VStack(spacing: 12) {
                                HStack {
                                    Circle()
                                        .fill(Color.green)
                                        .frame(width: 12, height: 12)
                                    TextField("Pickup location", text: $pickupLocation)
                                        .textFieldStyle(.plain)
                                }
                                .padding()
                                .background(Color(.systemGray6))
                                .cornerRadius(12)
                                
                                HStack {
                                    Circle()
                                        .fill(Color.red)
                                        .frame(width: 12, height: 12)
                                    TextField("Destination", text: $destinationLocation)
                                        .textFieldStyle(.plain)
                                }
                                .padding()
                                .background(Color(.systemGray6))
                                .cornerRadius(12)
                            }
                            
                            // Request Ride Button
                            Button(action: {
                                requestRide()
                            }) {
                                HStack {
                                    Text("Request Ride")
                                        .font(.headline)
                                    Spacer()
                                    Image(systemName: "arrow.right")
                                }
                                .foregroundColor(.white)
                                .padding()
                                .frame(maxWidth: .infinity)
                                .background(
                                    pickupLocation.isEmpty || destinationLocation.isEmpty
                                    ? Color.gray
                                    : Color.blue
                                )
                                .cornerRadius(12)
                            }
                            .disabled(pickupLocation.isEmpty || destinationLocation.isEmpty)
                        }
                        .padding()
                    }
                }
                .background(Color(.systemBackground))
                .cornerRadius(20, corners: [.topLeft, .topRight])
                .shadow(radius: 10)
            }
        }
    }
    
    private func requestRide() {
        // Simulate ride request
        let now = Date()
        let pickupLoc = Location(
            name: pickupLocation,
            latitude: 37.7749,
            longitude: -122.4194
        )
        let destLoc = Location(
            name: destinationLocation,
            latitude: 37.7849,
            longitude: -122.4094
        )
        
        let initialRide = Ride(
            id: UUID().uuidString,
            riderId: "temp-rider-id", // This should come from auth
            driverId: nil,
            pickupLocation: pickupLoc,
            destinationLocation: destLoc,
            status: .searching,
            driverName: nil,
            driverRating: nil,
            estimatedArrival: nil,
            fare: nil,
            createdAt: now,
            updatedAt: now
        )
        currentRide = initialRide
        
        // Simulate finding a driver after 2 seconds
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            let updatedRide = Ride(
                id: initialRide.id,
                riderId: initialRide.riderId,
                driverId: "temp-driver-id",
                pickupLocation: initialRide.pickupLocation,
                destinationLocation: initialRide.destinationLocation,
                status: .matched,
                driverName: "John Doe",
                driverRating: 4.8,
                estimatedArrival: Date().addingTimeInterval(300), // 5 minutes
                fare: 15.50,
                createdAt: initialRide.createdAt,
                updatedAt: Date()
            )
            currentRide = updatedRide
        }
    }
}

struct ActiveRideView: View {
    let ride: Ride
    
    var body: some View {
        VStack(spacing: 16) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(ride.status == .searching ? "Finding a driver..." : "Driver on the way")
                        .font(.headline)
                    if let driverName = ride.driverName {
                        Text(driverName)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                }
                Spacer()
                if let rating = ride.driverRating {
                    HStack(spacing: 4) {
                        Image(systemName: "star.fill")
                            .foregroundColor(.yellow)
                        Text(String(format: "%.1f", rating))
                            .font(.subheadline)
                    }
                }
            }
            
            if let arrival = ride.estimatedArrival {
                HStack {
                    Image(systemName: "clock")
                    Text("Arriving in \(formatTime(arrival))")
                }
                .font(.subheadline)
                .foregroundColor(.secondary)
            }
            
            if let fare = ride.fare {
                HStack {
                    Text("Estimated fare:")
                        .foregroundColor(.secondary)
                    Spacer()
                    Text("$\(String(format: "%.2f", fare))")
                        .font(.headline)
                }
            }
            
            Button(action: {
                // Cancel ride action
            }) {
                Text("Cancel Ride")
                    .foregroundColor(.red)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.red.opacity(0.1))
                    .cornerRadius(12)
            }
        }
        .padding()
    }
    
    private func formatTime(_ date: Date) -> String {
        let minutes = Int(date.timeIntervalSinceNow / 60)
        return "\(minutes) min"
    }
}

extension View {
    func cornerRadius(_ radius: CGFloat, corners: UIRectCorner) -> some View {
        clipShape(RoundedCorner(radius: radius, corners: corners))
    }
}

struct RoundedCorner: Shape {
    var radius: CGFloat = .infinity
    var corners: UIRectCorner = .allCorners
    
    func path(in rect: CGRect) -> Path {
        let path = UIBezierPath(
            roundedRect: rect,
            byRoundingCorners: corners,
            cornerRadii: CGSize(width: radius, height: radius)
        )
        return Path(path.cgPath)
    }
}

#Preview {
    RiderView()
}

