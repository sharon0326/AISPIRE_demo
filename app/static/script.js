// Smooth scrolling for nav links
document.querySelectorAll("nav a[href^='#']").forEach(anchor => {
    anchor.addEventListener("click", function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });
  
  // Register button scrolls to pricing section
  const registerBtn = document.querySelector(".register-btn");
  if (registerBtn) {
    registerBtn.addEventListener("click", () => {
      const plans = document.querySelector(".plans");
      if (plans) {
        plans.scrollIntoView({ behavior: "smooth" });
      }
    });
  }
  
  // Try Now button highlights testimonials
  const tryNowBtn = document.querySelector(".try-now-btn");
  if (tryNowBtn) {
    tryNowBtn.addEventListener("click", () => {
      const section = document.querySelector(".testimonials");
      if (section) {
        section.scrollIntoView({ behavior: "smooth" });
        
        section.style.transition = "background-color 0.6s";
        section.style.backgroundColor = "#e0f7fa";
        setTimeout(() => {
          section.style.backgroundColor = "";
        }, 1200);
      }
    });
  }
  
  // Dashboard functionality
  document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    // Resume upload handling
    const resumeUpload = document.getElementById('resume-upload');
    const pdfUpload = document.querySelector('.pdf-upload');
    
    console.log('Resume upload element:', resumeUpload);
    console.log('PDF upload area:', pdfUpload);
    
    if (resumeUpload && pdfUpload) {
      // Make the entire upload area clickable
      pdfUpload.addEventListener('click', function(e) {
        console.log('Upload area clicked');
        resumeUpload.click();
      });
      
      resumeUpload.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
          const file = e.target.files[0];
          console.log('Resume uploaded:', file.name);
          
          // Create FormData object to send file to server
          const formData = new FormData();
          formData.append('resume', file);
          
          // Show loading state
          pdfUpload.classList.add('uploading');
          
          // ===== BACKEND INTEGRATION CODE =====
          // 后端接口代码 - Backend API Integration
          // 1. 发送文件到后端解析 - Send file to backend for parsing
          /*
          fetch('/api/parse-resume', {
            method: 'POST',
            body: formData
          })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            // 处理解析后的数据 - Handle parsed data
            console.log('Parsed resume data:', data);
            
            // 这里可以更新UI显示解析结果 - Update UI to show parsed results
            // displayParsedResume(data);
          })
          .catch(error => {
            console.error('Error parsing resume:', error);
            alert('Error uploading resume. Please try again.');
          })
          .finally(() => {
            pdfUpload.classList.remove('uploading');
          });
          */
          
          // 临时提示 - Temporary alert for testing
          setTimeout(() => {
            alert('Resume uploaded: ' + file.name + '\n\nIn production, this would send the file to the backend API for parsing.');
            pdfUpload.classList.remove('uploading');
          }, 1000);
        }
      });
    }
    
    // 消息发送功能 - Message sending functionality
    const messageInput = document.querySelector('.message-input input');
    const sendButton = document.querySelector('.send-button');
    
    if (messageInput && sendButton) {
      // 发送消息的函数 - Function to send message
      function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
          console.log('Sending message:', message);
          
          // ===== BACKEND INTEGRATION CODE =====
          // 后端接口代码 - Backend API Integration
          /*
          fetch('/api/send-message', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
          })
          .then(response => response.json())
          .then(data => {
            // 处理后端响应 - Handle backend response
            console.log('Response:', data);
            
            // 这里可以添加消息到聊天界面 - Add message to chat interface
            // addMessageToChat(message, data.response);
          })
          .catch(error => {
            console.error('Error sending message:', error);
          });
          */
          
          // 清空输入框 - Clear input field
          messageInput.value = '';
          
          // 临时提示 - Temporary alert for testing
          alert('Message sent: ' + message + '\n\nIn production, this would send the message to the backend API.');
        }
      }
      
      // 点击发送按钮 - Click send button
      sendButton.addEventListener('click', sendMessage);
      
      // 按回车键发送 - Press Enter to send
      messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          sendMessage();
        }
      });
    }
  });
  