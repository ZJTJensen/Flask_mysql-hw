SELECT
    comments.comment AS comment,
    comments.created_at AS comment_time,
    users.first_name as user
FROM
    comments
		JOIN
	comments on comments.messages_id = messages.id
        JOIN
    users ON comments.users_id = users.id
