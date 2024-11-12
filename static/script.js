    async function postTweet() {
      const tweetContent = document.getElementById('tweetContent').value;
      if (tweetContent.trim() === '') return;
    
      const isTweetToxic = await checkToxicity(tweetContent);
      console.log("Returning isTweetToxic: ",isTweetToxic)
      if (isTweetToxic==='True') {
        alert('Your words are against our community guidelines.');
      }
      else{
      // Post the tweet if it's not toxic
      const tweetContainer = document.createElement('div');
      tweetContainer.className = 'tweet';
    
      const tweetText = document.createElement('div');
      tweetText.className = 'tweet-content';
      tweetText.textContent = tweetContent;
    
      const commentsSection = document.createElement('div');
      commentsSection.className = 'comments';
    
      const commentBox = document.createElement('div');
      commentBox.className = 'comment-box';
    
      const commentInput = document.createElement('textarea');
      commentInput.placeholder = 'Write a comment...';
    
      const commentButton = document.createElement('button');
      commentButton.textContent = 'Comment';
      
      commentButton.onclick = async function() {
        const commentContent = commentInput.value;
        if (commentContent.trim() === '') return;
    
        const isCommentToxic = await checkToxicity(commentContent);
        if (isCommentToxic === 'True') {
          alert('Your comment is against our community guidelines.');
        }
        else{
        // Post the comment if it's not toxic
        const comment = document.createElement('div');
        comment.className = 'comment';
        comment.textContent = commentContent;
        commentsSection.appendChild(comment);
        alert('Your comment is successfully posted.');
        commentInput.value = '';
        }
      };
    
      commentBox.appendChild(commentInput);
      commentBox.appendChild(commentButton);
  
      tweetContainer.appendChild(tweetText);
      tweetContainer.appendChild(commentBox);
      tweetContainer.appendChild(commentsSection);
    
      document.getElementById('tweets').prepend(tweetContainer);
      alert('Your tweet is successfully posted.');
      document.getElementById('tweetContent').value = '';
     }
    }
    
    async function checkToxicity(text) {
      try {
        const response = await fetch('/check_toxicity', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: text }),
        });
        console.log(response)
        if (!response.ok) {
          console.error('Error:', response.statusText);
          return false;  // Assume not toxic if an error occurs
        }
    
        const result = await response.json();
        console.log(result)
        console.log("Result is toxic or not: ",result.isToxic)
        return result.isToxic;
      } catch (error) {
        console.error('Error checking toxicity:', error);
        return false;  // Assume not toxic if an error occurs
      }
    }
    