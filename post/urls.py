
from django.urls import path
from .import views

urlpatterns = [


    path("<slug:slug>/<slug:slug2>",views.PostView.as_view(),name='post'),
    path("<slug:slug>/<slug:slug2>/<str:pk>/reply",views.ReplyView.as_view(),name='reply'),

    path("<slug:slug>/create/create_text_post",views.CreateTextBasedPost.as_view(),name='create-text-post'),
    path("<slug:slug>/create/create_image_post",views.CreateImageBasedPost.as_view(),name='create-image-post'),
    path("<slug:slug>/create/create_video_post",views.CreateVideoBasedPost.as_view(),name='create-video-post'),

    path('upvote/<int:post_id>/', views.upvote, name='upvote'),
    path('downvote/<int:post_id>/', views.downvote, name='downvote'),

    path('upvote-comment/<int:comment_id>/', views.upvote_comment, name='upvote-comment'),
    path('downvote-comment/<int:comment_id>/', views.downvote_comment, name='downvote-comment'),

    path('upvote-reply-comment/<int:reply_id>/', views.upvote_reply, name='upvote-reply'),
    path('downvote-reply-comment/<int:reply_id>/', views.downvote_reply, name='downvote-reply'),


    path('delete-comment/<int:pk>/', views.DeleteCommentView.as_view(), name='delete-comment'),
    path('<slug:slug>/<slug:slug2>/update-comment/<int:pk>/', views.UpdateCommentView.as_view(), name='update-comment'),


    path('update-reply/<slug:slug>/<slug:slug2>/<int:pk>/<int:pk2>/', views.UpdateReplyView.as_view(), name='update-reply'),
    path('delete-reply/<int:pk>/', views.DeleteReplyView.as_view(), name='delete-reply'),
  


    path('delete-post/<slug:slug>/', views.DeletePostView.as_view(), name='delete-post'),
    path('update-post/<slug:slug>/', views.UpdatePostView.as_view(), name='update-post'),

  

]
