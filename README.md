BlocklandForumsAPI
==================

An API to access the forums information.
To use:

    from blocklandforums import BlocklandForums
    bl = BlocklandForums()
    files = bl.categories["Files"]
    board = files.boards["Add-Ons"]
    topics = board.get_topics() #soon support for more pages :P
    topic = topics[5]
    posts = topic.get_posts(page=2)
    post = posts[0]
    post_author = post.poster
