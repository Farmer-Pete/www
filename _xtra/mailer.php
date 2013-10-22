<?php

$from_email = $_POST['email'] == '' ? Null : $_POST['email'];
$result = array();
$success = True;

if ($_POST['name'] == '') {
    $from_name = Null;
    $result[] = 'Thanks for your message!';
} else {
    $from_name = $_POST['name'];
    $result[] = 'Thanks, ' . $from_name . ', for taking the time to write me!';
}

$result[] = 'I do read each and every email and appreciate your feedback :)';

if ($_POST['email'] == '') {
    $from_email = Null;
    $result[] = "<em>Please note that you didn't provide an email address. I'll be sure to read your message, but I won't be able to reply to you.</em>";
} else {
    $from_email = $_POST['email'];
    $result[] = "I'll reply to as soon as I can, but it may be a couple of days depending on my work schedule.";
}

$to = strrev('mf.liamtsaf@ytfelxunil'); # Reverse to hide from web bugs
$subject = $from_name == Null ? "A non-a mouse" : $from_name . ' commented on "' . $_POST['title'] . '"';
$message = wordwrap($_POST['comment'], 70, "\n");
if ($from_email == Null) {
    $message .= "\n\n** Sender provided no email. DO NOT REPLY TO THIS MESSAGE **\n\n";
    $headers = '';
} else {
    $headers = "Reply-To: $from_email";
}

$message .= "\n\n--\n\nReferring post:" . $_POST['url'];

mail($to, $subject, $message, $headers);

?>
<html>
<head>
    <title>Thanks for your message!</title>
    <link href="/theme/css/template.css" rel="stylesheet" type="text/css" media="screen" />
    <style type="text/css">
        #page #main #main_inner {
            padding: 1em;
        }
        #page #main {
            margin-top: 5em;
        }
        p {
            margin-top: 1em;
        }
        .codehilite {
            padding: 1.5em;
            font-size: 1em;
        }
    </style>
</head>
<body>
    <div id="page">
        <div id="main">
            <div id="main_inner">
                <?php foreach ($result as $paragraph): ?>
                    <p><?php echo $paragraph; ?></p>
                <?php endforeach; ?>
                <?php if ($success): ?>
                    <p>For your records, you sent the following email to me:</p>
<pre class="codehilite">
Name: <?php echo $from_name ?>

Email: <?php echo $from_email ?>

Message:

<?php echo wordwrap(htmlspecialchars($_POST['comment'], 70, "\n")); ?>
</pre>
                    <p>
                <?php endif; ?>
                    <a href="<?php echo $_POST['url'];?>">&lt;&#151&#151 Return to previous page</a>
                </p>
            </div>
        </div> 
    </div>
</body>
</html>
