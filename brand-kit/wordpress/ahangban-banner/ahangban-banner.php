<?php
/**
 * Plugin Name:       Ahangban Banner — «سرت بیاد»
 * Plugin URI:        https://github.com/Masoumiofficial/ahangban
 * Description:       بنر اسلایدر آهنگ‌بان با شورت‌کد <code>[ahangban_banner]</code>؛ عنوان و نام هنرمند به‌صورت متن واقعی رندر می‌شوند تا خوانا، قابل‌جست‌وجو و قابل‌ترجمه باشند.
 * Version:           1.0.0
 * Requires at least: 6.2
 * Requires PHP:      7.4
 * Author:            Ahangban
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       ahangban-banner
 *
 * @package Ahangban_Banner
 */

defined( 'ABSPATH' ) || exit;

define( 'AHANGBAN_BANNER_VERSION', '1.0.0' );
define( 'AHANGBAN_BANNER_URL', plugin_dir_url( __FILE__ ) );

/**
 * ثبت استایل با هندل مشخص؛ بارگذاری در هر صفحه فقط در صورت نیاز.
 */
function ahangban_banner_register_style() {
	wp_register_style(
		'ahangban-banner',
		AHANGBAN_BANNER_URL . 'assets/ahangban-banner.css',
		array(),
		AHANGBAN_BANNER_VERSION
	);
}
add_action( 'wp_enqueue_scripts', 'ahangban_banner_register_style' );

/**
 * اگر شورت‌کد در محتوای برگه هست، استایل در head بارگذاری شود (بدون پرش چیدمان).
 * اگر شورت‌کد از ویجت/بیلدر بیاید، خودِ شورت‌کد آن را در ادامهٔ صفحه صف می‌کند.
 */
function ahangban_banner_maybe_enqueue_style() {
	if ( ! is_singular() ) {
		return;
	}

	$post = get_post();
	if ( $post && has_shortcode( (string) $post->post_content, 'ahangban_banner' ) ) {
		wp_enqueue_style( 'ahangban-banner' );
	}
}
add_action( 'wp_enqueue_scripts', 'ahangban_banner_maybe_enqueue_style', 20 );

/**
 * ساخت رشتهٔ اتریبیوت‌ها با اسکیپ کامل.
 *
 * @param array $attrs نام ⇒ مقدار؛ مقدار null نادیده گرفته می‌شود.
 * @return string
 */
function ahangban_banner_attr_string( array $attrs ) {
	$parts = array();

	foreach ( $attrs as $name => $value ) {
		if ( null === $value || '' === $value ) {
			continue;
		}
		$parts[] = sprintf( '%s="%s"', esc_attr( $name ), esc_attr( $value ) );
	}

	return implode( ' ', $parts );
}

/**
 * الگوی بلوک برای درج یک‌کلیکی در ویرایشگر.
 */
function ahangban_banner_register_patterns() {
	if ( ! function_exists( 'register_block_pattern' ) ) {
		return;
	}

	if ( function_exists( 'register_block_pattern_category' ) ) {
		register_block_pattern_category(
			'ahangban',
			array( 'label' => __( 'آهنگ‌بان', 'ahangban-banner' ) )
		);
	}

	register_block_pattern(
		'ahangban/banner-saret-biad',
		array(
			'title'       => __( 'بنر ویژهٔ آهنگ — «سرت بیاد»', 'ahangban-banner' ),
			'description' => __( 'پس‌زمینهٔ ۶۴۰×۳۶۰ با جای کاور در یک‌سوم چپ و عنوان فارسی در دو سوم راست. پیوند دکمه و کاور را جایگزین کنید.', 'ahangban-banner' ),
			'categories'  => array( 'ahangban' ),
			'content'     => "<!-- wp:shortcode -->\n[ahangban_banner]\n<!-- /wp:shortcode -->",
		)
	);
}
add_action( 'init', 'ahangban_banner_register_patterns' );

/**
 * خروجی بنر.
 *
 * @param array  $atts    ویژگی‌های شورت‌کد.
 * @param string $content محتوای میان تگ‌ها؛ استفاده نمی‌شود.
 * @return string
 */
function ahangban_banner_shortcode( $atts, $content = '' ) {
	unset( $content );

	$atts = shortcode_atts(
		array(
			'title'     => __( 'سرت بیاد', 'ahangban-banner' ),
			'artist'    => __( 'مهدی جهانی', 'ahangban-banner' ),
			'meta'      => __( 'تک‌آهنگ', 'ahangban-banner' ),
			'cta'       => __( 'گوش بده', 'ahangban-banner' ),
			'href'      => '',
			'cover'     => '',
			'cover_alt' => __( 'کاور «سرت بیاد» از مهدی جهانی', 'ahangban-banner' ),
			'bg'        => AHANGBAN_BANNER_URL . 'assets/banner-saret-biad-640x360.png',
			'bg2x'      => AHANGBAN_BANNER_URL . 'assets/banner-saret-biad-1280x720.png',
			'tag'       => 'h2',
			'loading'   => 'eager',
			'class'     => '',
		),
		$atts,
		'ahangban_banner'
	);

	$title = trim( wp_strip_all_tags( $atts['title'] ) );
	if ( '' === $title ) {
		return '';
	}

	wp_enqueue_style( 'ahangban-banner' );

	$tag = strtolower( (string) $atts['tag'] );
	if ( ! in_array( $tag, array( 'h1', 'h2', 'h3', 'p', 'div' ), true ) ) {
		$tag = 'h2';
	}

	$loading = ( 'lazy' === $atts['loading'] ) ? 'lazy' : 'eager';
	$bg      = esc_url_raw( $atts['bg'] );
	$bg2x    = esc_url_raw( $atts['bg2x'] );
	$href    = esc_url( $atts['href'] );
	$cover   = esc_url( $atts['cover'] );
	$uid     = wp_unique_id( 'hb-banner-' );

	$classes = array( 'hb-banner' );
	foreach ( preg_split( '/\s+/', (string) $atts['class'] ) as $extra ) {
		$extra = sanitize_html_class( $extra );
		if ( $extra ) {
			$classes[] = $extra;
		}
	}

	$media_attrs = array(
		'class'         => 'hb-banner__media',
		'src'           => $bg,
		'srcset'        => ( $bg2x && $bg2x !== $bg ) ? sprintf( '%1$s 1x, %2$s 2x', $bg, $bg2x ) : null,
		'width'         => '640',
		'height'        => '360',
		'alt'           => '',
		'loading'       => $loading,
		'decoding'      => 'async',
		'fetchpriority' => ( 'eager' === $loading ) ? 'high' : null,
	);

	$cover_attrs = array(
		'class'    => 'hb-banner__cover-img',
		'src'      => $cover,
		'width'    => '160',
		'height'   => '160',
		'alt'      => $atts['cover_alt'],
		'loading'  => 'lazy',
		'decoding' => 'async',
	);

	ob_start();
	?>
<div id="<?php echo esc_attr( $uid ); ?>" class="<?php echo esc_attr( implode( ' ', $classes ) ); ?>" dir="rtl">
	<img <?php echo ahangban_banner_attr_string( $media_attrs ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- مقادیر در سازنده اسکیپ شده‌اند. ?>>
	<div class="hb-banner__cover<?php echo $cover ? '' : ' hb-banner__cover--empty'; ?>">
		<?php if ( $cover ) : ?>
			<img <?php echo ahangban_banner_attr_string( $cover_attrs ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- مقادیر در سازنده اسکیپ شده‌اند. ?>>
		<?php endif; ?>
	</div>
	<div class="hb-banner__body">
		<?php if ( '' !== trim( (string) $atts['artist'] ) ) : ?>
			<p class="hb-banner__artist"><?php echo esc_html( $atts['artist'] ); ?></p>
		<?php endif; ?>
		<<?php echo $tag; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- از فهرست مجاز. ?> class="hb-banner__title"><?php echo esc_html( $title ); ?></<?php echo $tag; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- از فهرست مجاز. ?>>
		<?php if ( '' !== trim( (string) $atts['meta'] ) ) : ?>
			<p class="hb-banner__meta"><?php echo esc_html( $atts['meta'] ); ?></p>
		<?php endif; ?>
		<?php if ( $href ) : ?>
			<a class="hb-banner__cta" href="<?php echo esc_url( $href ); ?>"><?php echo esc_html( $atts['cta'] ); ?></a>
		<?php endif; ?>
	</div>
</div>
	<?php
	return (string) ob_get_clean();
}
add_shortcode( 'ahangban_banner', 'ahangban_banner_shortcode' );
