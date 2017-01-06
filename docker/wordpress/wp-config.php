<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'wordpress');

/** MySQL database username */
define('DB_USER', 'root');

/** MySQL database password */
define('DB_PASSWORD', '');

/** MySQL hostname */
define('DB_HOST', '127.0.0.1');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8mb4');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'q1R1)t`;S9TESXo22Q6|$:D`MN$59/sM[%+LArug}fY2u<#K,]NkBbep@=6dd3<|');
define('SECURE_AUTH_KEY',  '9q[!x5x4aGZw 7^ng3I5&^Hc.tI~eE2G^U)?(01(yVi{#vDCMb 30tLzdbUQ!<7.');
define('LOGGED_IN_KEY',    ':$GF@-4lqcCE.,@,M4T%1?,KP9-}*q-6Prf0vCy3`4?g-vko+,gJzi w,T1f1TfN');
define('NONCE_KEY',        '-KL|R?190*tMCCUnf1AK6?YpHd9DI_k)T=^e3[>K`1E|4B*k/VFOvU1W:eAQPSTi');
define('AUTH_SALT',        'pK(;pyUa;PK(SR0_>7k:bIWz1X5}Mzw}h$rfXu-H !RTv q`~g%~$6|E /Q}R/Sv');
define('SECURE_AUTH_SALT', 'HdY7OAP~[/O+FT{j6@@cS5`+H!EkL*CS*79F?i_/NB,&DW5Tk(abN]1/^;@hu%yt');
define('LOGGED_IN_SALT',   'l|d5%9&d<K-%8NTrjHXHgVnBy>bX<1c2Rs6TJ!z|rf#WA1*0jJ>TIQ:cP(Iqz#uw');
define('NONCE_SALT',       'rQ%MHCb<Q,Z7uObE7xT21jfTQ<QdB[,S^46XiyP;SuAeDv9khagk+Iu)9HabF?mc');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
