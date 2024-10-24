-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Sep 14, 2024 at 04:40 AM
-- Server version: 10.1.19-MariaDB
-- PHP Version: 5.6.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+03:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `final_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `bases`
--

CREATE TABLE `bases` (
  `base_id` int(11) NOT NULL,
  `base_x_coordinate` float DEFAULT NULL,
  `base_y_coordinate` float DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bases`
--

INSERT INTO `bases` (`base_id`, `base_x_coordinate`, `base_y_coordinate`, `is_available`) VALUES
(1, 383.2, 66.4, 1),
(2, 289.2, 115.7, 1),
(3, 330.7, 154.8, 1),
(4, 192, 139.8, 1),
(5, 327, 280.7, 1);

-- --------------------------------------------------------

--
-- Table structure for table `deliveries`
--

CREATE TABLE `deliveries` (
  `delivery_id` int(11) NOT NULL,
  `drone_id` int(11) DEFAULT NULL,
  `drop_id` int(11) DEFAULT NULL,
  `pickup_id` int(11) DEFAULT NULL,
  `is_collected` tinyint(4) NOT NULL,
  `is_delivered` tinyint(4) NOT NULL,
  `requested_date` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `deliveries`
--

INSERT INTO `deliveries` (`delivery_id`, `drone_id`, `drop_id`, `pickup_id`, `is_collected`, `is_delivered`, `requested_date`) VALUES
(1, NULL, 4, 2, 0, 0, 1726281571);

-- --------------------------------------------------------

--
-- Table structure for table `drones`
--

CREATE TABLE `drones` (
  `drone_id` int(11) NOT NULL,
  `battery_percentage` int(11) DEFAULT NULL,
  `is_fault` tinyint(1) DEFAULT NULL,
  `is_detouring` tinyint(4) NOT NULL,
  `velocity` int(11) DEFAULT NULL,
  `drone_x_coordinate` float DEFAULT NULL,
  `drone_y_coordinate` float DEFAULT NULL,
  `drone_z_coordinate` float DEFAULT NULL,
  `real_x` float NOT NULL,
  `real_y` float NOT NULL,
  `real_z` float NOT NULL,
  `is_package_load` tinyint(1) DEFAULT NULL,
  `is_package_unload` tinyint(1) DEFAULT NULL,
  `last_communication` double DEFAULT NULL,
  `planned_start_time` double DEFAULT NULL,
  `step_index` int(11) DEFAULT NULL,
  `base_id` int(11) DEFAULT NULL,
  `ready_for_delivery` tinyint(1) DEFAULT NULL,
  `last_moved` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `drones`
--

INSERT INTO `drones` (`drone_id`, `battery_percentage`, `is_fault`, `is_detouring`, `velocity`, `drone_x_coordinate`, `drone_y_coordinate`, `drone_z_coordinate`, `real_x`, `real_y`, `real_z`, `is_package_load`, `is_package_unload`, `last_communication`, `planned_start_time`, `step_index`, `base_id`, `ready_for_delivery`, `last_moved`) VALUES
(9, 86, 0, 0, 0, 327, 280.7, -1, 327, 280.7, -1, 0, 0, 0, NULL, NULL, 5, 1, 0),
(10, 90, 0, 0, 0, 383.2, 66.4, -1, 383.2, 66.4, -1, 0, 0, 0, NULL, NULL, 1, 1, 0),
(11, 98, 0, 0, 0, 289.2, 115.7, -1, 289.2, 115.7, -1, 0, 0, 0, NULL, NULL, 2, 1, 0),
(12, 95, 0, 0, 0, 330.7, 154.8, -1, 330.7, 154.8, -1, 0, 0, 0, NULL, NULL, 3, 1, 0),
(13, 88, 0, 0, 0, 192, 139.8, -1, 192, 139.8, -1, 0, 0, 0, NULL, NULL, 4, 1, 0),
(14, 86, 0, 0, 0, 327, 280.7, -1, 327, 280.7, -1, 0, 0, 0, NULL, NULL, 5, 1, 0),
(15, 90, 0, 0, 0, 383.2, 66.4, -1, 383.2, 66.4, -1, 0, 0, 0, NULL, NULL, 1, 1, 0),
(16, 98, 0, 0, 0, 289.2, 115.7, -1, 289.2, 115.7, -1, 0, 0, 0, NULL, NULL, 2, 1, 0),
(17, 95, 0, 0, 0, 330.7, 154.8, -1, 330.7, 154.8, -1, 0, 0, 0, NULL, NULL, 3, 1, 0),
(18, 88, 0, 0, 0, 192, 139.8, -1, 192, 139.8, -1, 0, 0, 0, NULL, NULL, 4, 1, 0),
(19, 86, 0, 0, 0, 327, 280.7, -1, 327, 280.7, -1, 0, 0, 0, NULL, NULL, 5, 1, 0),
(20, 90, 0, 0, 0, 383.2, 66.4, -1, 383.2, 66.4, -1, 0, 0, 0, NULL, NULL, 1, 1, 0),
(21, 98, 0, 0, 0, 289.2, 115.7, -1, 289.2, 115.7, -1, 0, 0, 0, NULL, NULL, 2, 1, 0),
(22, 95, 0, 0, 0, 330.7, 154.8, -1, 330.7, 154.8, -1, 0, 0, 0, NULL, NULL, 3, 1, 0),
(23, 88, 0, 0, 0, 192, 139.8, -1, 192, 139.8, -1, 0, 0, 0, NULL, NULL, 4, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `drop_locations`
--

CREATE TABLE `drop_locations` (
  `drop_id` int(11) NOT NULL,
  `drop_x_coordinate` float DEFAULT NULL,
  `drop_y_coordinate` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `drop_locations`
--

INSERT INTO `drop_locations` (`drop_id`, `drop_x_coordinate`, `drop_y_coordinate`) VALUES
(1, 164.7, 332.4),
(2, 309.9, 398.9),
(3, 58.2, 307.5),
(4, 188.2, 333.6),
(5, 240.1, 31);

-- --------------------------------------------------------

--
-- Table structure for table `obstacles`
--

CREATE TABLE `obstacles` (
  `id` int(11) NOT NULL,
  `x_min` double DEFAULT NULL,
  `x_max` double DEFAULT NULL,
  `y_min` double DEFAULT NULL,
  `y_max` double DEFAULT NULL,
  `z_min` double DEFAULT NULL,
  `z_max` double DEFAULT NULL,
  `t_start` double DEFAULT NULL,
  `t_end` double DEFAULT NULL,
  `value` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `obstacles`
--

INSERT INTO `obstacles` (`id`, `x_min`, `x_max`, `y_min`, `y_max`, `z_min`, `z_max`, `t_start`, `t_end`, `value`) VALUES
(1, 301.4, 307.2, 133.4, 139, 0, 134.4, 0, 10000000000, 10),
(2, 184.9, 196.5, 273.4, 279.1, 0, 156.9, 0, 10000000000, 10),
(3, 69.3, 78.5, 184.6, 201.8, 0, 75.1, 0, 10000000000, 10),
(4, 252.6, 268.3, 52.7, 67.8, 0, 42.4, 0, 10000000000, 10),
(5, 171.2, 174.7, 120.2, 133, 0, 167.3, 0, 10000000000, 10),
(6, 17, 28.7, 90.3, 102.5, 0, 156.4, 0, 10000000000, 10),
(7, 252.2, 260, 4.8, 10.4, 0, 150.8, 0, 10000000000, 10),
(8, 221.3, 235.9, 367.6, 386.7, 0, 50.4, 0, 10000000000, 10),
(9, 298.4, 312.2, 177.2, 188.5, 0, 151.8, 0, 10000000000, 10),
(10, 15.9, 27.9, 213.6, 226.6, 0, 37.1, 0, 10000000000, 10),
(11, 12.7, 22.9, 366.3, 383.1, 0, 41.2, 0, 10000000000, 10),
(12, 356, 364.1, 313.9, 320.6, 0, 150.9, 0, 10000000000, 10),
(13, 359.3, 362.5, 283.2, 299.9, 0, 140.8, 0, 10000000000, 10),
(14, 88.4, 102.3, 307, 317.4, 0, 199.8, 0, 10000000000, 10),
(15, 122.8, 139.8, 246.3, 257.1, 0, 55.6, 0, 10000000000, 10),
(16, 228.6, 239.1, 258.1, 261.4, 0, 190.7, 0, 10000000000, 10),
(17, 316.9, 324, 75.9, 91.3, 0, 39.5, 0, 10000000000, 10),
(18, 210.3, 228.4, 34.8, 38.9, 0, 65, 0, 10000000000, 10),
(19, 76.1, 96, 77.6, 96.7, 0, 110.7, 0, 10000000000, 10),
(20, 238.4, 251.8, 75.4, 79.5, 0, 58.9, 0, 10000000000, 10),
(21, 228.6, 246.7, 154.5, 167.2, 0, 162.7, 0, 10000000000, 10),
(22, 11.1, 26.9, 301.9, 320.6, 0, 62.4, 0, 10000000000, 10),
(23, 199.7, 210.6, 289.3, 297.2, 0, 186.2, 0, 10000000000, 10),
(24, 60.6, 74.6, 21, 39.4, 0, 74.2, 0, 10000000000, 10),
(25, 109.2, 113, 273.5, 289.6, 0, 189.1, 0, 10000000000, 10),
(26, 256, 271.6, 149.5, 165, 0, 164.2, 0, 10000000000, 10),
(27, 120.7, 138.7, 340.9, 354.1, 0, 181, 0, 10000000000, 10),
(28, 79, 82.2, 126.5, 140.1, 0, 157, 0, 10000000000, 10),
(29, 152.6, 160.5, 152.7, 161.9, 0, 156.1, 0, 10000000000, 10),
(30, 129, 138.7, 108.2, 127.3, 0, 105.8, 0, 10000000000, 10),
(31, 255.7, 271.2, 284.9, 302.3, 0, 45.3, 0, 10000000000, 10),
(32, 312, 318.5, 317.3, 322, 0, 115.9, 0, 10000000000, 10),
(33, 174.5, 189.1, 170.9, 182.1, 0, 32, 0, 10000000000, 10),
(34, 169.1, 173.4, 161.2, 165, 0, 129.1, 0, 10000000000, 10),
(35, 94.3, 110.4, 390.5, 396.4, 0, 179.5, 0, 10000000000, 10),
(36, 64.4, 82.2, 370, 376.8, 0, 114.4, 0, 10000000000, 10),
(37, 333.8, 341.4, 231.4, 246.8, 0, 54.6, 0, 10000000000, 10),
(38, 126.8, 132.4, 366.4, 382.6, 0, 194.7, 0, 10000000000, 10),
(39, 15.1, 33.1, 266.9, 282.8, 0, 63.5, 0, 10000000000, 10),
(40, 34.2, 53.3, 156.7, 172.8, 0, 94.4, 0, 10000000000, 10),
(41, 184.8, 190, 41.3, 45.4, 0, 30.7, 0, 10000000000, 10),
(42, 279, 284.2, 83.2, 87.2, 0, 72.7, 0, 10000000000, 10),
(43, 127.4, 134.2, 48, 64.7, 0, 44.2, 0, 10000000000, 10),
(44, 243.3, 257.7, 141.6, 148.2, 0, 174.2, 0, 10000000000, 10),
(45, 145.2, 156.5, 78.3, 97.1, 0, 45, 0, 10000000000, 10),
(46, 389.9, 396.1, 368.9, 384.2, 0, 58.4, 0, 10000000000, 10),
(47, 0.2, 15.4, 17.8, 24.4, 0, 57.2, 0, 10000000000, 10),
(48, 31.5, 47.8, 390.9, 394.6, 0, 85.1, 0, 10000000000, 10),
(49, 280.7, 297, 207.4, 220.3, 0, 125, 0, 10000000000, 10),
(50, 244.9, 254.9, 205.8, 213.5, 0, 91.7, 0, 10000000000, 10),
(51, 323.4, 340.5, 388.4, 399.2, 0, 182.9, 0, 10000000000, 10),
(52, 21.5, 33.2, 171.3, 179.3, 0, 92.3, 0, 10000000000, 10),
(53, 349.6, 368.5, 153.9, 159.6, 0, 144.8, 0, 10000000000, 10),
(54, 118, 129.8, 131.1, 136.2, 0, 142, 0, 10000000000, 10),
(55, 64.5, 79.2, 268.2, 277.1, 0, 187.5, 0, 10000000000, 10),
(56, 199.5, 205.3, 227.6, 247.5, 0, 179.5, 0, 10000000000, 10),
(57, 227.4, 241.2, 53.4, 67.5, 0, 88.4, 0, 10000000000, 10),
(58, 337, 356.1, 201.9, 215, 0, 101.9, 0, 10000000000, 10),
(59, 26.6, 42.1, 329.4, 346.6, 0, 146.5, 0, 10000000000, 10),
(60, 280.3, 284.2, 366.2, 379.7, 0, 132.4, 0, 10000000000, 10),
(61, 88.8, 100.2, 361.6, 377.8, 0, 32.3, 0, 10000000000, 10),
(62, 310.3, 326.6, 339.5, 355.3, 0, 32.2, 0, 10000000000, 10),
(63, 154.9, 163.3, 210, 221.8, 0, 76.4, 0, 10000000000, 10),
(64, 47.5, 59.8, 150.1, 155.6, 0, 62.2, 0, 10000000000, 10),
(65, 312.9, 329.4, 11.5, 30.5, 0, 81.4, 0, 10000000000, 10),
(66, 353.6, 361.1, 138.2, 152.9, 0, 61.3, 0, 10000000000, 10),
(67, 109.6, 118.1, 92.7, 96.6, 0, 144.6, 0, 10000000000, 10),
(68, 254.7, 273, 37.2, 40.2, 0, 181.7, 0, 10000000000, 10),
(69, 369.4, 378.4, 329.2, 346.9, 0, 74.2, 0, 10000000000, 10),
(70, 99.7, 113.8, 237.6, 242, 0, 178.8, 0, 10000000000, 10),
(71, 297.1, 312.2, 292.8, 311.7, 0, 46.7, 0, 10000000000, 10),
(72, 154.7, 174.7, 322.4, 342.4, 0, 200, 0, 10000000000, 8),
(73, 373.2, 393.2, 56.4, 76.4, 0, 200, 0, 10000000000, 8),
(74, 280.6, 300.6, 48.3, 68.3, 0, 200, 0, 10000000000, 8),
(75, 299.9, 319.9, 388.9, 408.9, 0, 200, 0, 10000000000, 8),
(76, 279.2, 299.2, 105.7, 125.7, 0, 200, 0, 10000000000, 8),
(77, 48.2, 68.2, 297.5, 317.5, 0, 200, 0, 10000000000, 8),
(78, 139.3, 159.3, 388.4, 408.4, 0, 200, 0, 10000000000, 8),
(79, 320.7, 340.7, 144.8, 164.8, 0, 200, 0, 10000000000, 8),
(80, 364.1, 384.1, 279.9, 299.9, 0, 200, 0, 10000000000, 8),
(81, 178.2, 198.2, 323.6, 343.6, 0, 200, 0, 10000000000, 8),
(82, 182, 202, 129.8, 149.8, 0, 200, 0, 10000000000, 8),
(83, 263, 283, 185.8, 205.8, 0, 200, 0, 10000000000, 8),
(84, 317, 337, 270.7, 290.7, 0, 200, 0, 10000000000, 8),
(85, 230.1, 250.1, 21, 41, 0, 200, 0, 10000000000, 8),
(86, 126, 146, 280.8, 300.8, 0, 200, 0, 10000000000, 8);

-- --------------------------------------------------------

--
-- Table structure for table `pickup_locations`
--

CREATE TABLE `pickup_locations` (
  `pickup_id` int(11) NOT NULL,
  `pickup_x_coordinate` float DEFAULT NULL,
  `pickup_y_coordinate` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pickup_locations`
--

INSERT INTO `pickup_locations` (`pickup_id`, `pickup_x_coordinate`, `pickup_y_coordinate`) VALUES
(1, 290.6, 58.3),
(2, 149.3, 398.4),
(3, 374.1, 289.9),
(4, 273, 195.8),
(5, 136, 290.8);

-- --------------------------------------------------------

--
-- Table structure for table `steps`
--

CREATE TABLE `steps` (
  `id` int(11) NOT NULL,
  `step_index` int(11) NOT NULL,
  `drone_x_coordinate` float DEFAULT NULL,
  `drone_y_coordinate` float DEFAULT NULL,
  `drone_z_coordinate` float DEFAULT NULL,
  `drone_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bases`
--
ALTER TABLE `bases`
  ADD PRIMARY KEY (`base_id`);

--
-- Indexes for table `deliveries`
--
ALTER TABLE `deliveries`
  ADD PRIMARY KEY (`delivery_id`),
  ADD KEY `drone_id` (`drone_id`),
  ADD KEY `drop_id` (`drop_id`),
  ADD KEY `pickup_id` (`pickup_id`);

--
-- Indexes for table `drones`
--
ALTER TABLE `drones`
  ADD PRIMARY KEY (`drone_id`),
  ADD KEY `base_id` (`base_id`);

--
-- Indexes for table `drop_locations`
--
ALTER TABLE `drop_locations`
  ADD PRIMARY KEY (`drop_id`);

--
-- Indexes for table `obstacles`
--
ALTER TABLE `obstacles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pickup_locations`
--
ALTER TABLE `pickup_locations`
  ADD PRIMARY KEY (`pickup_id`);

--
-- Indexes for table `steps`
--
ALTER TABLE `steps`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `drone_id` (`drone_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bases`
--
ALTER TABLE `bases`
  MODIFY `base_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `deliveries`
--
ALTER TABLE `deliveries`
  MODIFY `delivery_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `drones`
--
ALTER TABLE `drones`
  MODIFY `drone_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;
--
-- AUTO_INCREMENT for table `drop_locations`
--
ALTER TABLE `drop_locations`
  MODIFY `drop_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `obstacles`
--
ALTER TABLE `obstacles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=907;
--
-- AUTO_INCREMENT for table `pickup_locations`
--
ALTER TABLE `pickup_locations`
  MODIFY `pickup_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `steps`
--
ALTER TABLE `steps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `deliveries`
--
ALTER TABLE `deliveries`
  ADD CONSTRAINT `deliveries_ibfk_1` FOREIGN KEY (`drone_id`) REFERENCES `drones` (`drone_id`),
  ADD CONSTRAINT `deliveries_ibfk_2` FOREIGN KEY (`drop_id`) REFERENCES `drop_locations` (`drop_id`),
  ADD CONSTRAINT `deliveries_ibfk_3` FOREIGN KEY (`pickup_id`) REFERENCES `pickup_locations` (`pickup_id`);

--
-- Constraints for table `drones`
--
ALTER TABLE `drones`
  ADD CONSTRAINT `drones_ibfk_1` FOREIGN KEY (`base_id`) REFERENCES `bases` (`base_id`);

--
-- Constraints for table `steps`
--
ALTER TABLE `steps`
  ADD CONSTRAINT `steps_ibfk_1` FOREIGN KEY (`drone_id`) REFERENCES `drones` (`drone_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


-- INSERT INTO `steps` (`step_index`, `drone_x_coordinate`, `drone_y_coordinate`, `drone_z_coordinate`, `drone_id`)
-- VALUES
-- -- Steps for Drone 1 (drone_id = 1)
-- (1, 192, 139.8, 40, 23),
-- (2, 192, 139.8, 44, 24);


