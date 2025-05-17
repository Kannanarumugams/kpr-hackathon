<?php
$servername = "localhost";
$username = "root"; // Change if needed
$password = ""; // Change if needed
$dbname = "job_registeration";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve form data (make sure names match HTML form fields)
$name = isset($_POST['name']) ? $conn->real_escape_string($_POST['name']) : '';
$village = isset($_POST['village']) ? $conn->real_escape_string($_POST['village']) : '';
$district = isset($_POST['district']) ? $conn->real_escape_string($_POST['district']) : '';
$contact = isset($_POST['contact']) ? $conn->real_escape_string($_POST['contact']) : '';
$age = isset($_POST['age']) ? intval($_POST['age']) : 0; // Ensure age is an integer
$work = isset($_POST['work']) ? $conn->real_escape_string($_POST['work']) : '';
$experience = isset($_POST['experience']) ? intval($_POST['experience']) : 0; // Ensure experience is an integer
$salary = isset($_POST['salary']) ? floatval($_POST['salary']) : 0.0; // Ensure salary is a float

// Validate required fields
if (empty($name) || empty($village) || empty($district) || empty($contact)) {
    die("Error: Name, village, district, and contact are required fields.");
}

// Corrected SQL query using actual column names from your database
$sql = "INSERT INTO form (name, village, `district-`, contact, age, work, experience, salary) 
        VALUES ('$name', '$village', '$district', '$contact', $age, '$work', $experience, $salary)";

if ($conn->query($sql) === TRUE) {
    echo "Registration successful!";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

// Close connection
$conn->close();
?>