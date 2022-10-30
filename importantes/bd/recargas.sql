--PATH C:\Python27;%PATH%

-- phpMyAdmin SQL Dump
-- version 3.2.0.1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 27-10-2011 a las 20:57:18
-- Versión del servidor: 5.1.36
-- Versión de PHP: 5.3.0

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Base de datos: `recargas_celular`
--

create database recargas_celular;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recargas`
--

CREATE TABLE IF NOT EXISTS `recargas` (
  `codRecarga` int(11) NOT NULL AUTO_INCREMENT,
  `codEmpresa` varchar(100) NOT NULL,
  `Compania` varchar(100) NOT NULL,
  `nroCelular` varchar(15) NOT NULL,
  `monto` varchar(10) NOT NULL,
  `lugar` varchar(500) NOT NULL,
  `fechaRecarga` varchar(8) NOT NULL,
  `horaRecarga` varchar(6) NOT NULL,
  `fechaIngreso` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`codRecarga`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=36 ;

--
-- Volcar la base de datos para la tabla `recargas`
--