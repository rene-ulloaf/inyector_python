-- phpMyAdmin SQL Dump
-- version 3.2.0.1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 09-11-2011 a las 21:44:36
-- Versión del servidor: 5.1.36
-- Versión de PHP: 5.3.0

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Base de datos: `recargas_celular`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cia`
--

DROP TABLE IF EXISTS `cia`;
CREATE TABLE IF NOT EXISTS `cia` (
  `id_cia` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `vigente` bit(1) NOT NULL,
  PRIMARY KEY (`id_cia`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Volcar la base de datos para la tabla `cia`
--

INSERT INTO `cia` (`id_cia`, `nombre`, `vigente`) VALUES
(1, 'Entel', b'1'),
(2, 'Movistar', b'1'),
(3, 'Claro', b'1'),
(4, 'BellSouth', b'0'),
(5, 'smartcom', b'0'),
(6, 'telefonica', b'0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recargas`
--

DROP TABLE IF EXISTS `recargas`;
CREATE TABLE IF NOT EXISTS `recargas` (
  `id_recarga` int(11) NOT NULL AUTO_INCREMENT,
  `id_cia` int(11) NOT NULL,
  `cod_cia` varchar(50) NOT NULL,
  `id_telefono` int(11) NOT NULL,
  `monto` bigint(20) NOT NULL,
  `fecha_recarga` varchar(8) NOT NULL,
  `hora_recarga` varchar(6) NOT NULL,
  `fecha_ingreso` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_recarga`),
  UNIQUE KEY `id_cia` (`id_cia`,`id_telefono`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Volcar la base de datos para la tabla `recargas`
--


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursal`
--

DROP TABLE IF EXISTS `sucursal`;
CREATE TABLE IF NOT EXISTS `sucursal` (
  `id_sucursal` int(11) NOT NULL AUTO_INCREMENT,
  `id_cia` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `vigente` bit(1) NOT NULL,
  PRIMARY KEY (`id_sucursal`),
  UNIQUE KEY `indx_suc` (`id_cia`,`nombre`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=19 ;

--
-- Volcar la base de datos para la tabla `sucursal`
--

INSERT INTO `sucursal` (`id_sucursal`, `id_cia`, `nombre`, `vigente`) VALUES
(1, 1, 'Maipu', b'1'),
(2, 2, 'Maipu', b'1'),
(3, 3, 'Maipu', b'1'),
(4, 1, 'rinconada', b'0'),
(5, 3, 'santiago', b'1'),
(6, 3, 'pte. alto', b'1'),
(7, 3, 'Renca', b'1'),
(8, 3, 'Las Condes', b'1'),
(9, 3, 'La Florida', b'1'),
(10, 3, 'suc. Maipu', b'0'),
(11, 1, 'La Florida', b'1'),
(12, 1, 'Providencia', b'1'),
(13, 1, 'Huechuraba', b'1'),
(14, 1, 'pte. alto', b'1'),
(16, 2, 'Pudahuel', b'1'),
(17, 2, 'Santiago', b'1'),
(18, 2, 'pte. alto', b'1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `suc_reg`
--

DROP TABLE IF EXISTS `suc_reg`;
CREATE TABLE IF NOT EXISTS `suc_reg` (
  `id_suc_reg` int(11) NOT NULL AUTO_INCREMENT,
  `id_recarga` int(11) NOT NULL,
  `id_sucursal` int(11) NOT NULL,
  PRIMARY KEY (`id_suc_reg`),
  UNIQUE KEY `id_recarga` (`id_recarga`,`id_sucursal`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Volcar la base de datos para la tabla `suc_reg`
--


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `telefono`
--

DROP TABLE IF EXISTS `telefono`;
CREATE TABLE IF NOT EXISTS `telefono` (
  `id_telefono` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `id_cia` int(11) NOT NULL,
  `numero` varchar(25) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL,
  `vigente` bit(1) NOT NULL,
  PRIMARY KEY (`id_telefono`),
  UNIQUE KEY `numero` (`numero`),
  UNIQUE KEY `numero_2` (`numero`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=22 ;

--
-- Volcar la base de datos para la tabla `telefono`
--

INSERT INTO `telefono` (`id_telefono`, `id_usuario`, `id_cia`, `numero`, `vigente`) VALUES
(1, 1, 1, '66087405', b'1'),
(2, 2, 2, '96087405', b'1'),
(3, 3, 3, '99999999', b'1'),
(4, 4, 1, '966087405', b'0'),
(5, 5, 3, '88888888', b'1'),
(6, 6, 3, '77777777', b'1'),
(7, 7, 3, '66666666', b'1'),
(8, 8, 3, '55555555', b'1'),
(9, 9, 3, '44444444', b'1'),
(10, 10, 3, '33333333', b'1'),
(11, 11, 1, '90883033', b'1'),
(12, 13, 1, '92729057', b'1'),
(15, 12, 1, '92929057', b'1'),
(16, 1, 1, '94833018', b'1'),
(17, 14, 1, '75195569', b'1'),
(18, 15, 2, '96187405', b'1'),
(19, 16, 2, '96287405', b'1'),
(20, 17, 2, '96387405', b'1'),
(21, 18, 2, '96487405', b'1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(500) NOT NULL,
  `id_cia` int(11) NOT NULL,
  `vigente` bit(1) NOT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=19 ;

--
-- Volcar la base de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `id_cia`, `vigente`) VALUES
(1, 'René Ulloa', 1, b'1'),
(2, 'cliente movistar', 2, b'1'),
(3, 'cliente claro', 3, b'1'),
(4, 'cliente no vigente', 1, b'1'),
(5, 'cliente claro 2', 3, b'1'),
(6, 'cliente claro 3', 3, b'1'),
(7, 'cliente claro 3', 3, b'1'),
(8, 'cliente claro 4', 3, b'1'),
(9, 'cliente claro 4', 3, b'1'),
(10, 'cliente claro 5', 3, b'1'),
(11, 'Luis Ulloa', 1, b'1'),
(12, 'Juan Jose', 1, b'1'),
(13, 'Ingrid Fuenzalida', 1, b'1'),
(14, 'Evelyn Rojas', 1, b'1'),
(15, 'cliente movistar 2', 2, b'1'),
(16, 'cliente movistar 3', 2, b'1'),
(17, 'cliente movistar 3', 2, b'1'),
(18, 'cliente movistar 4', 2, b'1');
