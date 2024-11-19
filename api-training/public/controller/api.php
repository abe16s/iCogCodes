<?php

/**
 * The public-facing functionality of the plugin.
 *
 * @package    Api_Training
 * @subpackage Api_Training/public
 * @author     Khalid <khalinoid@gmail.com>
 */
class Api_Training_APIs {

    public function __construct()
    {
        add_shortcode('my_shortcode', [$this, 'api_training_shortcodes']);
    }

    function api_training_shortcodes(){
        $response = '';
        if (isset($_POST['api_text'])) {
            $text = sanitize_text_field($_POST['api_text']);
            $response = $this->send_post_request($text);
        }

        ob_start();
        ?>
        <form method="post" style="margin-bottom: 20px;">
            <label for="api_text">Enter Text:</label>
            <input type="text" id="api_text" name="api_text" value="<?php echo isset($text) ? esc_attr($text) : ''; ?>" required style="margin-right: 10px;">
            <button type="submit">Send</button>
        </form>

        <?php if ($response): 
            $response_data = json_decode($response, true);
            if (is_array($response_data)): ?>
                <div style="border: 1px solid #ddd; padding: 15px; background-color: #f9f9f9; border-radius: 5px; margin-top: 10px;">
                    <h3 style="color: #333;">API Response:</h3>
                    <p><strong>Text:</strong> <?php echo esc_html($response_data['text']); ?></p>
                    <p><strong>Sentiment:</strong> <?php echo esc_html(ucfirst($response_data['sentiment'])); ?></p>
                    <p><strong>Confidence:</strong> <?php echo esc_html(number_format($response_data['confidence'] * 100, 2)); ?>%</p>
                </div>
            <?php else: ?>
                <div style="color: #a94442; background-color: #f2dede; border: 1px solid #ebccd1; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <p>Invalid response format.</p>
                </div>
            <?php endif; ?>
        <?php elseif (isset($text)): ?>
            <div style="color: #a94442; background-color: #f2dede; border: 1px solid #ebccd1; padding: 10px; border-radius: 5px; margin-top: 10px;">
                <p>No response received. Please try again.</p>
            </div>
        <?php endif; ?>

        <?php
        return ob_get_clean();
    }

    function send_post_request($text){
        $url = 'http://127.0.0.1:5000/predict';
        
        $body = json_encode([
            'text' => $text
        ]);

        $args = [
            'body'        => $body,
            'headers'     => [
                'Content-Type' => 'application/json',
            ],
            'method'      => 'POST',
            'data_format' => 'body',
        ];

        $response = wp_remote_post($url, $args);

        if (is_wp_error($response)) {
            error_log('Error: ' . $response->get_error_message());
            return null;
        }

        return wp_remote_retrieve_body($response);
    }
}
