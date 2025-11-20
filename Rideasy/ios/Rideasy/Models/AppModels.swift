//
//  AppModels.swift
//  Rideasy
//
//  Created by Ahmed Kadri on 20.11.25.
//

import Foundation
import CoreLocation

enum UserMode: String, Codable {
    case rider = "rider"
    case driver = "driver"
}

enum RideStatus: String, Codable {
    case searching = "searching"
    case matched = "matched"
    case driverArriving = "driverArriving"
    case inProgress = "inProgress"
    case completed = "completed"
    case cancelled = "cancelled"
}

struct Location: Identifiable, Codable {
    let id: String
    let name: String
    let latitude: Double
    let longitude: Double
    
    var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }
    
    init(id: String = UUID().uuidString, name: String, latitude: Double, longitude: Double) {
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    }
}

struct Ride: Identifiable, Codable {
    let id: String
    let riderId: String
    let driverId: String?
    let pickupLocation: Location
    let destinationLocation: Location
    var status: RideStatus
    var driverName: String?
    var driverRating: Double?
    var estimatedArrival: Date?
    var fare: Double?
    let createdAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case riderId = "rider_id"
        case driverId = "driver_id"
        case pickupLocation = "pickup_location"
        case destinationLocation = "destination_location"
        case status
        case driverName = "driver_name"
        case driverRating = "driver_rating"
        case estimatedArrival = "estimated_arrival"
        case fare
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

struct DriverRide: Identifiable {
    let id = UUID()
    let pickupLocation: Location
    let destinationLocation: Location
    let riderName: String
    let riderRating: Double
    let fare: Double
    var status: RideStatus
}

// MARK: - Authentication Models

struct User: Identifiable, Codable {
    let id: String
    let email: String
    let username: String
    let fullName: String?
    let phoneNumber: String?
    let userMode: UserMode
    let rating: Double
    let isOnline: Bool
    let currentLatitude: Double?
    let currentLongitude: Double?
    let createdAt: Date
    let updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case email
        case username
        case fullName = "full_name"
        case phoneNumber = "phone_number"
        case userMode = "user_mode"
        case rating
        case isOnline = "is_online"
        case currentLatitude = "current_latitude"
        case currentLongitude = "current_longitude"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}

struct AuthResponse: Codable {
    let accessToken: String
    let tokenType: String
    let user: User
    
    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case tokenType = "token_type"
        case user
    }
}

struct LoginRequest: Codable {
    let email: String
    let password: String
}

struct RegisterRequest: Codable {
    let email: String
    let username: String
    let password: String
    let fullName: String?
    let phoneNumber: String?
    let userMode: UserMode
}
