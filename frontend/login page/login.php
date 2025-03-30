<?php
session_start();
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    if ($username == 'admin' && $password == 'password') {
        $_SESSION['user'] = $username;
        echo "Login successful!";
    } else {
        echo "Invalid credentials";
    }
}
?>