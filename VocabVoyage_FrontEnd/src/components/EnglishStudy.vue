<template>
  <div class="top_container">

    <div class="top_section">
        <!-- 上面的部分内容 -->


        <div class="menu" >
          <SearchContainer @select="handleWordSelect"></SearchContainer>

          <el-button style="margin-left: 16px;" circle @click="drawer = true">
            <div style="width: 30px; height: 30px; overflow: hidden; border-radius: 50%;">
                <img src="http://vocab-voyage.oss-cn-beijing.aliyuncs.com/kk.jpg" alt="User Avatar" style="width: 100%; height: auto;" />
            </div>
            
          </el-button>
        </div>
        <!-- search -->


        <!-- user photo -->


    </div>




  </div>

  <div class="body_container">
    <div class="container">
      <div class="bottom-section">
        <div class="left-section">
          <!-- 左边的部分内容 -->

          <!-- TODO 高度写死问题 -->
          <el-scrollbar height="800px">
            <div v-for="(word, index) in words" :key="index" class="scrollbar-demo-item">
              <div class="card" @click="handleCardClick(word)">
                <a class="card1" href="#">
                  <div class="word_and_sound">
                    <p>{{ word.spell }}</p>
                    <el-button  
                      class="sound_button"
                      size="small" 
                      circle :icon="VideoPlay" 
                      @click="() => handle_sound(word.spell)" 
                      style="font-size: 24px; border-color: transparent; background-color: inherit;"
                    />
                  </div>
                  <!-- <p class="small">test meaning here</p> -->
                  <!-- <p class="small">{{ word.meaning }}</p> -->
                  <!-- <p class="small">{{ word.description }}</p> -->
                  <div class="go-corner" href="#">
                    <div class="go-arrow">
                      →
                    </div>
                  </div>
                </a>
              </div>
            </div>
          </el-scrollbar>

        </div>
        <div class="right-section">
          <div class="right-top">
            <!-- 右边上面的部分内容 -->

            <el-tabs type="border-card" class="detail_screen" v-model="activeTab">
                <el-tab-pane name="Describe" label="Describe" class="markdown-card">
                    <!-- <div>123123</div> -->
                     <!-- TODO高度写死问题，滚动条问题 -->
                    <div v-html="selectedWordInfo.value ? selectedWordInfo.value.description : ''" style="max-height: 600px; overflow-y: auto; "></div>
                </el-tab-pane>
                <el-tab-pane name="Chat" label="Chat">

                  <div class="chat-container">
                    <div class="chat-messages">
                      <div v-for="(message, index) in messages" :key="index" class="message">
                        <div :class="['message-bubble', message.role]" v-html="message.content">


                        </div>
                      </div>
                    </div>
                    <!-- <div class="chat-input">
                      <input
                        v-model="newMessage"
                        @keyup.enter="sendMessage"
                        placeholder="Type your message..."
                      />
                      <button @click="sendMessage">Send</button>
                    </div> -->
                  </div>


                </el-tab-pane>

            </el-tabs>



          </div>
          <div class="right-bottom">
            <!-- 右边下面的部分内容 -->
             <div v-if="activeTab == 'Describe'" class="three_button">
              <el-button type="primary" size="large" @click="sendMemoryResult(1)">认识</el-button>
              <el-button type="warning" size="large" @click="sendMemoryResult(2)">模糊</el-button>
              <el-button type="danger" size="large" @click="sendMemoryResult(3)">忘记</el-button>
             </div>



             <div v-else-if="activeTab == 'Chat'" class="chat-input">
              <textarea
                v-model="newMessage"
                @keyup.enter="sendMessage"
                placeholder="Try to ask..."
                style="width: 100%; height: 100%; box-sizing: border-box;padding: 10px; font-size: large; overflow-y: auto; resize: none;"
              />
                <!-- <input
                  v-model="newMessage"
                  @keyup.enter="sendMessage"
                  type="textarea"
                  placeholder="Try to ask..."
                /> -->
                <button @click="sendMessage">Send</button>
              </div>
          </div>
        </div>
      </div>
    </div>


    <el-drawer v-model="drawer" title="I am the title" :with-header="false">

      <el-button type="primary" @click="handleProfileClick">To Your Profile</el-button>

        
    </el-drawer>


  </div>

</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';

import { VideoPlay } from '@element-plus/icons-vue';
import { marked } from 'marked';
import { getWordById, getWordBySpell, memorizeWord } from "../api/word.js";
import router from '../router';
import SearchContainer from './SearchContainer.vue';
// import { modelChat } from '../api/model.js'

const drawer = ref(false)

const activeTab = ref('Chat'); // 默认选中 Describe 标签


// TODO循环页面
const handle_sound = (spell) => {
  const audioUrl = `http://dict.youdao.com/dictvoice?type=1&audio=${spell}`;
  const audio = new Audio(audioUrl);
  audio.play();
}




// 大模型对话函数部分

const messages = reactive([])
const newMessage = ref('')

// messages.push({ role: 'system', content: "我是你的私人英语老师，我不仅会给你解释这个单词的意思，我还会详细解释这个单词背后的一切！" })
const sendMessage = async () => {
  //TODO 没有进行集成到model.js，此处写死
  // await modelChat(newMessage.value, messages)
  if (newMessage.value.trim()) {
    const userMessage = marked(newMessage.value)
    messages.push({ role: 'user', content: userMessage })
    newMessage.value = ''

    const response = await fetch('http://localhost:8000/model/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ messages })
    })


    if (response.status === 200) {
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let assistantMessage = ''
      messages.push({ role: 'assistant', content: '', streaming: true })

      while (true) {
        const { value, done } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        assistantMessage += chunk

        //TODO 回复内容改成markdown实时渲染！！！！例如提示词：给我回复100字markdown格式
        // messages[messages.length - 1].content += marked(chunk)
        messages[messages.length - 1].content += chunk
      }



      messages[messages.length - 1].streaming = false
    } else {
      console.error('Error:', response.status)
    }
  }
}


// 组件挂载后解析 Markdown 内容
// onMounted(() => {)
//   selectedWordInfo.value.description = marked(selectedWordInfo.value.description)
// })



const handleWordSelect = async (word) => {
  // 处理从搜索框组件选中的单词

  console.log('Selected word:', word)


  const res = await getWordBySpell(word)
  console.log(res.data)

  if (res.code == '0') {
        console.log("未找到对应单词！");
        alert("未找到对应单词！")

    } else {
        console.log("成功找到单词：", res.data.data);

        handleCardClick(res.data.data)
        // selectedWordInfo.value = res.data; // 设置选中单词的信息

        activeTab.value = "Describe"
        console.log(selectedWordInfo)
    }

}

// 获取路由参数
const route = useRoute();
// const wordIds = JSON.parse(route.query.wordIds || '[35432, 37434 , 42413, 41435, 40436, 39437, 37438, 41439, 35740, 36041]'); // 解析传递的 wordIds

const wordIds = [35432, 37434 , 42413, 41435, 40436, 39437, 37438, 41439, 35740, 36041];

const words = reactive([]); // 用于存储单词详细信息
const selectedWordInfo = reactive({
  value: {
    description: '',

    // meaning: '',
    // spell: '',
    // id:"",

  }
}); // 新增响应式变量，用于存储选中单词的信息



onMounted(async () => {
  for (const id of wordIds) {
    const res = await getWordById(id)

    if(res.data.code == 1){
      res.data.data["id"] = id;

      words.push(res.data.data); // 将单词信息添加到数组中
    }else{
      console.log("获取单词失败")
    }

  }


});

// 处理卡片点击事件
const handleCardClick = (word) => {
  console.log("in handleclick:")

  selectedWordInfo.value = word; // 设置选中单词的信息

  console.log("selectedWordInfo:",selectedWordInfo.value)
  selectedWordInfo.value.description = marked(selectedWordInfo.value.description)

  activeTab.value = "Describe"

  // selectedDescription.value = marked(word.description); // 删除此行
};


const sendMemoryResult = async (memRes) => {
  if (selectedWordInfo.value.id) {

    const memorise_rank = ref({
      word_id: selectedWordInfo.value.id,
      mem_res: memRes
    })
    console.log(memorise_rank.value)
    const res = memorizeWord(memorise_rank.value)
    console.log("memorize res：",res)

  } else {
    console.error('No selected word ID available');
  }
}


const handleProfileClick = ()=>{
  router.push("/Personal").then(() => {
      window.location.reload(); // 刷新页面
  });
}





</script>



<style scoped>
@import "Card.less";
@import "ChatAssistent.less";
.top_section{
  width: 80%;

}
.menu{
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* width: 80%; */
}
.body_container{
  display: flex;
  justify-content: center;
  align-items: center;
/* TODO演示颜色，后续可删除或替换背景 */
  /* background-color: rgb(113, 17, 17); */
    background-color: rgba(113, 17, 17,0.3);
  /* 确保不出现滚动条 */
  overflow: hidden; 

  background-image: url("../../public/back2.png");
}
.container {
  display: flex;
  flex-direction: column;
  margin-top: 64px;
  /* 使整体占满视口高度，减去顶部固定高度 */
  height: calc(100vh - 64px); 

  width: 80%;

}

.top_container{
    position: fixed; /* 固定到页面顶部 */
    top: 0; /* 距离顶部0 */
    left: 0; /* 距离左侧0 */
    right: 0; /* 距离右侧0 */
    z-index: 1000; /* 确保在其他元素之上 */
    display: flex;
    justify-content: center;
    align-items: center;
    /* TODO演示颜色，后续可删除或替换背景 */
    /* background-color: rgb(17, 105, 163); */
      background-color: rgba(28, 212, 68,0.3);
    height: 64px;
}

.top-section {
  /* 上面部分自适应内容高度 */
  flex: 0 0 64px; 
  height: 64px;
}

.bottom-section {
  display: flex;
  flex: 1; /* 下面部分占满剩余空间 */
}

.left-section {
  flex: 0 0 25%; /* 左边部分宽度 */
  /* overflow-y: auto; 使左边部分可滚动 */
  padding:16px 16px 16px 0px;
  /* TODO演示颜色，后续可删除或替换背景 */
  /* background-color: rgb(28, 212, 68); */
    background-color: rgba(255, 255, 255, 0.3);

}




/* TODO单词和声音 */
.word_and_sound{

  display: flex;
  justify-content: space-between;
  align-items: center;

}

.sound_button{

  right: 10px;
}

.right-section {
  display: flex;
  flex-direction: column;
  flex: 1; /* 右边部分占满剩余空间 */

  height: 100%;

}

.right-top {
  /* 右边上面部分占80% */
  flex: 0 0 80%; 
  padding:16px 0px 16px 16px;
  /* TODO演示颜色，后续可删除或替换背景 */
  /* background-color: blue; */
  background-color: rgba(31, 22, 207, 0.3);
  /* height: 80%; */
  /* max-height: 80%; */
}

.right-bottom {
    /* 右边下面部分占20% */
    /* flex: 0 0 20%; */
  flex: 1; 
  padding:16px 0px 16px 16px;
  /* TODO演示颜色，后续可删除或替换背景 */
  /* background-color: rgb(0, 187, 255); */
  background-color: rgba(0, 187, 255,0.3);
  /* height: 20%; */
}

.detail_screen{
    height: 100%; /* 确保父元素的高度是100% */
    display: flex; /* 使用Flexbox布局 */
}

.markdown-card {
  max-height: 100%; /* 保持100%高度 */
  /* background-color: rgb(232, 11, 195); */
    /* padding-left: 20px; */
    /* text-align: left; */
  
  /* 自定义字体 */
  /* font-family: 'Arial', sans-serif; */
  /* font-size: 18px; */
  color: #333;
  /* background-color: aquamarine; */
  background-color: rgba(195, 62, 62, 0.3);
}



</style>
