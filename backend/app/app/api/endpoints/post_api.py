from fastapi import APIRouter,Depends,Form,File,UploadFile,status,Path,HTTPException,Query
from sqlalchemy.orm import Session
from api.deps import get_db
from typing import Annotated
from models.profile import Profile
from api.deps import getCurrentUser
from crud import crud_post
from schemas.post_schema import ShowAllPostDetail,UpdatePostSchema,PostDetail
from schemas.registration_schema import Message

router = APIRouter()

@router.get("/posts/me",response_model=list[PostDetail])
async def ShowAllPostOfMe(
                          db: Annotated[Session, Depends(get_db)],
                          profile: Annotated[Profile, Depends(getCurrentUser)]
):
    """
    Here , User can get their own Post's
    - **Post ID**
    - **Description**
    - **List of Image**
    - **Created Date**
    """
    return crud_post.getCurrentUserPosts(db=db,profile=profile)
    

@router.get("/show_all_post",response_model=list[ShowAllPostDetail])
async def showAllPost(
    db: Session = Depends(get_db)
):
    """
    Here, User can see Other user's post . Who is Public
    - **post_id**,
    - **created_at**, 
    - **profile_id**,
    - **profile_name**,
    - **profile_image**,
    - **List od post images** []
    - **description**,
    - **like_count**,
    - **comment_count**,
    - **Liked profile's**,
    - **Comment's and Commented Profile's**
    """
    posts = crud_post.getAllPost(db=db)
    return posts
    
@router.post("/create_post",status_code=status.HTTP_201_CREATED,response_model=Message)
async def createPost(db: Annotated[Session, Depends(get_db)],
                     post_img: Annotated[list[UploadFile], File()],
                     description: Annotated[str, Form()],
                     profile: Annotated[Profile, Depends(getCurrentUser)]
                     ):
    """
    Here user can create new post, 
    - **Post image**: User can add list of post image(more than one image) (Required)
    - **Description**: Post Description (Required)
    """
    post_obj = crud_post.createPost(db=db,profile=profile,list_of_image=post_img,description=description)
    return post_obj

@router.get("/post/{id}",response_model=ShowAllPostDetail)
async def showPostById(
                       db: Annotated[Session, Depends(get_db)],
                       profile: Annotated[Profile, Depends(getCurrentUser)],
                       id: Annotated[int, Path(...)]
):
    """
    Here, users can retrieve a post by its post ID.
     - **post_id**,
    - **created_at**, 
    - **profile_id**,
    - **profile_name**,
    - **profile_image**,
    - **List od post images** []
    - **description**,
    - **like_count**,
    - **comment_count**,
    - **Liked profile's**,
    - **Comment's and Commented Profile's**
    """
    db_post = crud_post.getPostById(db=db,post_id=id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
        
    return db_post
    
@router.put("/post/me/update/{post_id}", status_code=status.HTTP_200_OK,response_model=UpdatePostSchema)
async def updateThePost(
    post_id: int,
    db: Annotated[Session, Depends(get_db)],
    profile: Annotated[Profile, Depends(getCurrentUser)],
    description: Annotated[str | None, Form()]= None,
    images: Annotated[list[UploadFile] , File()] = None
):
    """
    Here, users can update their posts using their post ID.
    - **Post description**(Optional)
    - **Images**(Optional)
    """
    db_post = crud_post.getPost(db=db, post_id=post_id)
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if db_post.profile_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post"
        )

    updated_post = crud_post.updatePost(
        db=db,
        db_post=db_post,
        description=description,
        images=images
    )
    
    return UpdatePostSchema(
        description=updated_post.description,
        images=[image.image_path for image in updated_post.images]
    )



@router.delete("/post/me/delete/{post_id}",response_model=Message)
async def deleteMyPost(
                      db: Annotated[Session, Depends(get_db)],
                      profile: Annotated[Profile, Depends(getCurrentUser)],
                      post_id: int 
):
    """
    Here user can delete their post by post_id
    - **Post Id**:Required
    """
    db_post = crud_post.getPost(db=db, post_id=post_id)
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if db_post.profile_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post"
        )
        
    return Message(message=crud_post.deletePost(db=db,db_post=db_post))

"""
----------------------------------LIKE---------------------------------------------
"""
@router.post("/posts/{post_id}/like",response_model=Message)
async def likePost(
    db: Annotated[Session, Depends(get_db)],
    profile: Annotated[Profile, Depends(getCurrentUser)],
    post_id: int
):
    """
    Here User can like other post's
    - **Post Id**: Required
    """
    db_post = crud_post.getPost(db=db,post_id=post_id)
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    like = crud_post.likePost(db=db,post=db_post,profile=profile)
    return like
    
"""
---------------------------------COMMENT--------------------------------------------
"""
@router.post("/post/{post_id}/comment",response_model=Message)
async def commentPost(
    db: Annotated[Session, Depends(get_db)],
    profile: Annotated[Profile, Depends(getCurrentUser)],
    post_id: int,
    comment: Annotated[str , Query(...)]
):
    """
     Here User can comment other post's
    - **Post Id**: Required
    - **Comment**: Required
    """
    db_post = crud_post.getPost(db=db,post_id=post_id)
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    comment = crud_post.commentPost(db=db,post=db_post,profile=profile,comment=comment)
    return comment
    





    

    