<?php

// Builds list of Articles
function get_articles() {

    $articles = array();
    $exclude_dirs = array('.', '..', 'author', 'tag');

    foreach (scandir('.') as $category) {
        if (! is_dir($category) ) {
            continue; // If it isn't a directory, it isn't a category
        }

        if (array_search($category, $exclude_dirs) !== FALSE) {
            continue; // excluded directory
        }
        foreach (glob($category . '/*.html') as $article) {
            $articles[] = '/' . $article;
        }
    }

    return $articles;
}

// Exracts keywords from URL
function get_keywords($url) {
    $dot_position = strrpos($url, '.');
    if ($dot_position !== FALSE) {
        // Strip extension, if it exists
        $url = trim(substr($url, 0, $dot_position), ' /');
    }
    $url = str_replace(array('/','-','_','%20', '.'), ' ', strtolower($url)); // Normalize URL
    return explode(' ', $url);
}

// Counts the number of common keywords
function compute_score($keywords_a, $keywords_b) {
	return sizeof(array_values(array_intersect($keywords_a, $keywords_b)));
}

$closest = null;
$top_score = 0;
$url = $_SERVER["REQUEST_URI"];
$url_keywords = get_keywords($url);
foreach (get_articles() as $article) {

    $score = compute_score(get_keywords($article), $url_keywords);

    if ($score > $top_score) {
        $top_score = $score;
        $closest = $article;
    }
}

if ($closest != null) {
    header("HTTP/1.1 301 Moved Permanently");
    header("Location: http://".$_SERVER["HTTP_HOST"].$closest);
    exit();
} else {
    header('HTTP/1.0 404 Not Found');
    echo file_get_contents('404.html');
    exit();
}
?>
