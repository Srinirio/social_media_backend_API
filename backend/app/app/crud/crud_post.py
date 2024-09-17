from sqlalchemy.orm import Session
from sqlalchemy import and_, desc,or_
from schemas.post_schema import CommentSchema, LikeSchema, PostImageSchema, ShowAllPostDetail, UpdatePostSchema
from models.profile import Profile
from models.post import Post,PostImage
from models.registration import Registration
from models.like import Like
from models.comment import Comment
from fastapi import UploadFile,HTTPException,status
import os
from schemas.registration_schema import Message
import uuid
"""
get current user post
"""
def getCurrentUserPosts(db: Session,profile: Profile):
    posts = db.query(Post).filter(and_(Post.profile_id == profile.id,
                                       Post.is_active == True
                                       )).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No posts"
        )
    return [
        {
            "post_id": post.id,
            "description": post.description,
            "images": [image.image_path for image in post.images],
            "created_at": post.created_at
        }
        for post in posts
    ]


"""
Create post with list of image
"""
def createPost(db: Session, 
               profile: Profile, 
               list_of_image: list[UploadFile],
               description: str
               ):
    #create post without image
    db_post = Post(
        description = description,
        profile_id = profile.id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    for data in list_of_image:
        unique_filename = f"{uuid.uuid4()}.jpg"
        image_path = os.path.join("images", unique_filename)
        with open(image_path, "wb") as buffer:
             buffer.write(data.file.read())
        db_image = PostImage(
            image_path = image_path,
            post_id = db_post.id
        )
        db.add(db_image)
    db.commit()
    
    return Message(message="Post successfully created !!")
    
"""
get all Post
only profile who is public user
"""


def getAllPost(db: Session):
    all_posts = db.query(Post).join(Profile).filter(
        and_(Profile.is_active == False, Profile.is_private == False,Post.is_active == True)
    ).order_by(desc(Post.created_at)).all()

    posts = []
    for post in all_posts:
    
        image_list = [PostImageSchema(image_path=image.image_path) for image in post.images]
        
        like_list = [
            LikeSchema(
                post_id=like.post_id,
                profile_username=like.profile.username  
            )
            for like in post.likes
        ]
        like_count = len(like_list)

        comment_list = [
            CommentSchema(
                post_id=comment.post_id,
                profile_username=comment.profile.username,  
                comment=comment.comment
            )
            for comment in post.comments
        ]
        comment_count = len(comment_list)

        post_dict = ShowAllPostDetail(
            profile_id=post.profile.id,
            profile_name=post.profile.username,
            profile_image=post.profile.profile_image,
            post_id=post.id,
            description=post.description,
            created_at=post.created_at,
            images=image_list,
            like_count=like_count,
            comment_count=comment_count,
            likes=like_list,
            comments=comment_list
        )

        posts.append(post_dict)

    return posts


"""
get post by id
only public profile post
"""
def getPostById(db: Session,post_id: int):
    all_posts = db.query(Post).join(Profile).filter(
        and_(Profile.is_active == False, Profile.is_private == False, Post.id == post_id,Post.is_active == True)
    ).order_by(desc(Post.created_at)).all()

    post_dict ={}
    for post in all_posts:
    
        image_list = [PostImageSchema(image_path=image.image_path) for image in post.images]
        
        like_list = [
            LikeSchema(
                post_id=like.post_id,
                profile_username=like.profile.username  
            )
            for like in post.likes
        ]
        like_count = len(like_list)

        comment_list = [
            CommentSchema(
                post_id=comment.post_id,
                profile_username=comment.profile.username,  
                comment=comment.comment
            )
            for comment in post.comments
        ]
        comment_count = len(comment_list)

        post_dict = ShowAllPostDetail(
            profile_id=post.profile.id,
            profile_name=post.profile.username,
            profile_image=post.profile.profile_image,
            post_id=post.id,
            description=post.description,
            created_at=post.created_at,
            images=image_list,
            like_count=like_count,
            comment_count=comment_count,
            likes=like_list,
            comments=comment_list
        )
    return post_dict
"""
get post only by id
"""
def getPost(db: Session,post_id: int):
    return db.query(Post).filter(Post.id == post_id, Post.is_active == True).first()

"""
update post
"""
def updatePost(
    db: Session,
    db_post: Post,
    description: str | None = None,
    images: list[UploadFile] | None = None
):
    if description is not None:
        db_post.description = description

    if images:
        for image in db_post.images:
            os.remove(image.image_path)
            db.delete(image)
        
        for image_file in images:
            unique_filename = f"{uuid.uuid4()}.jpg"
            image_path = os.path.join("images", unique_filename)
            with open(image_path, "wb") as buffer:
                buffer.write(image_file.file.read())
            new_image = PostImage(
                image_path=image_path,
                post_id=db_post.id
            )
            db.add(new_image)

    db.commit()
    db.refresh(db_post)
    
    return db_post
    
"""
delete post
"""
def deletePost(db: Session,db_post: Post):
    for image in db_post.images:
        if os.path.exists(image.image_path):
            os.remove(image.image_path)
    db_post.is_active = False
    db.commit()
    return "Post successfully Deleted !!"

"""
------------------------------------LIKE---------------------------------------------
"""
def likePost(db: Session, post: Post, profile: Profile):

    existing_like = db.query(Like).filter(
        Like.post_id == post.id,
        Like.profile_id == profile.id
    ).first()
    
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this post"
        )

    like_the_post = Like(
        post_id=post.id,
        profile_id=profile.id
    )
    db.add(like_the_post)
    db.commit()
    
    return Message(message=f"You liked post id: {post.id}")

"""
comment post
"""
def commentPost(db: Session,post: Post,profile: Profile,comment: str):
    comment_post = Comment(
        post_id = post.id,
        profile_id = profile.id,
        comment = comment
    )
    db.add(comment_post)
    db.commit()
    return Message(message=f"You commented post id: {post.id}")
    