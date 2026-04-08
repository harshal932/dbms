// MongoDB Queries for Railway Management System
// Run these commands in your MongoDB client or inside a script context

// 1. Database Creation Context
// Note: If running in mongosh, you would run 'use railway_mgmt_mongo' before these commands.
// Here we just define the collections and operations.

const db = db.getSiblingDB('railway_mgmt_mongo');

// 2. Insert Train Catalog Information
db.trains_catalog.insertMany([
  {
    train_id: 1,
    amenities: ["WiFi", "AC", "Pantry", "Charging Ports"],
    classes: ["1AC", "2AC", "Sleeper"],
    avg_rating: 4.5,
    description: "Premium express train with top-notch amenities."
  },
  {
    train_id: 2,
    amenities: ["Non-AC", "General Seating"],
    classes: ["Sleeper", "General"],
    avg_rating: 3.2,
    description: "Standard local commute train."
  }
]);

// 3. Insert Passenger Feedback
db.passenger_feedback.insertMany([
  {
    passenger_name: "John Doe",
    train_id: 1,
    rating: 5,
    comments: "Excellent service and clean compartments.",
    date: new Date()
  },
  {
    passenger_name: "Jane Smith",
    train_id: 2,
    rating: 3,
    comments: "Average train, heavily crowded.",
    date: new Date()
  }
]);

// 4. Aggregation Query: Average Rating by Train
db.passenger_feedback.aggregate([
  { $group: { _id: "$train_id", averageRating: { $avg: "$rating" }, feedbackCount: { $sum: 1 } } }
]);

// 5. Indexing for Performance
db.trains_catalog.createIndex({ train_id: 1 });
db.passenger_feedback.createIndex({ train_id: 1, rating: -1 });
