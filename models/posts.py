class Posts:
    posts = {}
    
    def add(self, post):
        self.posts[post["id"]] = post

    def get(self, post_id):
        if post_id in self.posts:
            return self.posts[post_id]
        else:
            return None
