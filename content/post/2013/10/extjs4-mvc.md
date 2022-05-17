---
title:  ExtJs4 中的 MVC 应用架构
date: 2013-10-29
categories:  [ExtJs]
comments: on
tags: [extJs4, MVC]
id: 201310290930

---

### 一、ExtJs 4.x MVC 模式的原理与作用

大规模客户端应用通常不好实现不好组织也不好维护，因为功能和人力的不断增加，这些应用的规模很快就会超出掌控能力，ExtJS4 带来了一个新的应用架构，不但可以组织代码，还可以减少实现的内容。

<!-- more -->

新的应用架构遵照一个类 MVC 的模式，模型（Models）和控制器（Controllers）首次被引入。业界有很多种 MVC 架构，基本大同小异，ExtJS4 的定义如下：

a.**Model 模型**：模型是字段和它们的数据的集合，例如 User 模型带有 username 和 password 字段，模型知道如何持久化自己的数据，并且可以和其他模型关联，模型跟 ExtJS 3 中的 Record 类有点像（区别是，Record 只是单纯的扁平结构，而 Model 可以 nest），通常都用在 Store 中去展示 grid 和其他组件的数据。

b.**View 视图**：视图是组件的一种，专注于界面展示 – grid, tree, panel 都是 view。

c.**Controllers 控制器**：一个安放所有使你的 app 正确工作的代码的位置，具体一点应该是所有动作，例如如何渲染 view，如何初始化 model，和 app 的其他逻辑。

请注意：MVC 是一个框架，不是设计模式，更多的内容请参考：
[百度百科](http://baike.baidu.com/view/5432454.htm?fromId=31)

框架与设计模式虽然相似，但却有着根本的不同。设计模式是对在某种环境中反复出现的问题以及解决该问题的方案的描述，它比框架更抽象；框架可以用代码表示，也能直接执行或复用，而对模式而言只有实例才能用代码表示;设计模式是比框架更小的元素，一个框架中往往含有一个或多个设计模式，框架总是针对某一特定应用领域，但同一模式却可适用于各种应用。可以说，框架是软件，而设计模式是软件的知识。

简而言之：设计模式是大智慧，用来对软件设计进行分工；框架模式是小技巧，对具体问题提出解决方案，以提高代码复用率，降低耦合度。

### 二、ExtJs 4 MVC 框架搭建

#### 2.1、文件结构

ExtJS 4 应用都遵循一个统一的目录结构，每个应有都相同
MVC 中，所有类都放在`app`目录里面，这个目录可以有子目录，代表的是命名空间（一个子目录对应一个命名空间），使用不同的目录存放`views`,`models`,`controllers`,`stores`。当我们完成例子的时候，目录结构应该和下图一样：

![结构](//img.leense.site/post/2013/10/201310290930-1.png)

ExtJS SDK 必须的文件在目录 ext4 中，因此，`index.html`应该如下引入必须的 js 和 css 文件以及`app.js`

#### 2.2、在 app.js 中创建应用

<每个 ExtJS 4 的应用都从一个`Application`类的实例开始，这个实例包含应用的全局配置（例如应用的名字），这个实例也负责维护对全部模型、视图、控制器的引用的维护，还有一个`launch`函数，会在所有加载项加载完成之后调用。

首先需要选择一个全局命名空间，所有 ExtJS4 应用都需要有一个全局命名空间，以让所有应用中的类安放到其中：

```js
Ext.application({
  requires: ["Ext.container.Viewport"],
  name: "FWY", //定义的命名空间
  appFolder: "app", //指明应用的根目录
  launch: function() {
    Ext.create("Ext.container.Viewport", {
      layout: "fit",
      items: [
        {
          xtype: "panel",
          ---
title:  "标题",
          html: "内容"
        }
      ]
    });
  }
});
```

#### 2.3、定义一个控制器

控制器是应用的粘合剂，它们所作的事情就是监听事件并执行动作，继续我们的应用，创建一个控制器。创建`app/controller/Students.js`这个文件，并添加如下代码：

```js
Ext.define("FWY.controller.Students", {
  extend: "Ext.app.Controller",
  init: function() {
    console.debug("trigger controller init event");
  }
});
```

接下来在`app.js`中添加对 Students 控制器的引用：

```js
Ext.application({
...
controllers: [
    'Students'  //对应于controller文件夹下面的Students.js
],
...
});
```

当我们通过 index.html 查看应用，Students 控制器会被自动加载（因为在 app.js 的 Application 中增加了引用），并且 Students 的 init 方法会在 launch 之前调用。

`init`方法是个极好的地方，可以用来设置如何和 view 交互，通常都使用 Controller 的一个方法 control，control 方法使得监听 view 的事件变的容易，更新一下控制器，让它告知我们 panel 何时渲染：

```js
Ext.define("FWY.controller.Students", {
  extend: "Ext.app.Controller",
  init: function() {
    this.control({
      "viewport > panel": {
        render: this.onPanelRendered
      }
    });
  },
  onPanelRendered: function() {
    console.debug("该panel被渲染了");
  }
});
```

我们已经更新了 init 方法，使用 this.controll 给视图设置监听器。这个 controll 方法，使用最新的组件查询引擎（ComponentQuery）可以快速方便的找到页面上的组件。如果你对 ComponentQuery 不熟悉，可以查看 ComponentQuery 文档进行详细了解。简要一点，ComponentQuery 可以允许我们使用一个类似 css 选择器的方式找到组件。

在例子的 init 方法中我们应用了'viewport > panel'，可以解释为“查找 Viewport 直接后代中的所有 Panel 组件”，然后我们提供了一个对象匹配事件名称（这个例子中只用了 render）来提供响应函数。全部的影响就是无论哪个组件符合我们的选择器，当它的 render 事件触发时，我们的 onPanelRendered 函数都会被调用。

### 三、创建 ExtJs4 MVC 应用

#### 1、定义一个视图

直到现在，我们的应用只有很少代码，只有两个文
件 app.js 和 app/controller/Students.js，现在我们想增加一个 grid 显示所有系统中的学生列表，修改 3 处：

##### (1)、添加 view/List.js 视图

是时候更好的组织一下逻辑并开始使用视图了。

视图也是组件，通常都是 ExtJS 现有组件的子类，现在准备创建学生表，先创建 `app/view/student/List.js`
，添加代码：

```js
Ext.define("FWY.view.student.List", {
  extend: "Ext.grid.Panel",
  alias: "widget.studentlist",
  ---
title:  "学生信息列表",
  initComponent: function() {
    this.store = {
      fields: ["id", "name", "age", "sex"],
      data: [
        { id: 1, name: "zhangsan", age: 18, sex: "boy" },
        { id: 2, name: "lishi", age: 20, sex: "girl" }
      ]
    };
    this.columns = [
      { header: "编号", dataIndex: "id", flex: 1 },
      { header: "姓名", dataIndex: "name", flex: 1 },
      { header: "年龄", dataIndex: "age", flex: 1 },
      { header: "性别", dataIndex: "sex", flex: 1 }
    ];
    this.callParent(arguments);
  }
});
```

##### (2)、修改 controller/Students.js

我们的视图类就是一个普通的类，这个例子中我们扩展了 Grid 组件，并设置了别名，这样我们可以用 xtype 的方式调用这个组件，另外我们也添加了 store 和 columns 的配置。
接下来我们需要添加这个视图到 Students 控制器。因为我们用 'widget.studentlist' 设置了别名，所以我们可以使用 studentlist 作为 xtype，就像我们使用之前使用的 'panel'

```js
Ext.define('FWY.controller.Students', {
    extend: 'Ext.app.Controller',
    views: [
        'student.List'//添加view视图
    ],
    init: ...
    onPanelRendered: ...
});
```

##### (3)、修改 app.js，加载视图

接下来修改 app.js 让视图在 viewport 中渲染，需要修改 launch 方法

```js
Ext.application({
    ...
    launch: function() {
        Ext.create('Ext.container.Viewport', {
            layout: 'fit',
            items: {
                xtype: 'studentlist'
            }
        });
    }
});
```

唯一需要注意的是我们在 views 数组中指定了 'student.List' ，这告诉应用去自动加载对应的文件，ExtJS4 的动态加载系统会根据规则从服务器自动拉取文件，例如 student.List 就是规则，把.替换成/就是文件存放路径。刷新一下页面即可看到效果

#### 2、添加对列表的控制

分三步完成对对编辑窗体的控制

##### (1)、为 grid 绑定双击事件

注意 onPanelRendered 方法依然被调用，因为我们的 grid 依然满足 'viewport > panel' 选择器，因为我们的视图继承自 Grid ，从而继承自 Panel。现在我们需要收紧一下选择器，我们使用 xtype 作为选择器替换之前的 'viewport > panel' ，监听双击事件，以便继续做编辑用户信息：

```js
Ext.define("FWY.controller.Students", {
  extend: "Ext.app.Controller",
  views: ["student.List"],
  init: function() {
    this.control({
      studentlist: {
        itemdblclick: this.editStudent //添加行双击事件
      }
    });
  },
  editStudent: function(grid, record) {
    console.log("Double clicked on " + record.get("name"));
  }
});
```

注意我们更换了组件查询选择器为 'studentlist' ，监听的事件更改为 'itemdblclick' ，响应函数设置为 editStudent，现在只是简单的日志出双击行的 name 属性。

##### (2)、创建 view/student/Edit.js 视图

可以看到日志是正确的，但我们实际想做的是编辑用户信息，让我们现在做，创建一个新的视图 `app/view/student/Edit.js`

```js
Ext.define("FWY.view.student.Edit", {
  extend: "Ext.window.Window",
  alias: "widget.studentedit",
  ---
title:  "修改学生信息",
  layout: "fit",
  autoShow: true,
  initComponent: function() {
    this.items = [
      {
        xtype: "form",
        items: [
          {
            xtype: "textfield",
            name: "name",
            fieldLabel: "姓名"
          },
          {
            xtype: "textfield",
            name: "age",
            fieldLabel: "年龄"
          },
          {
            xtype: "textfield",
            name: "sex",
            fieldLabel: "性别"
          }
        ]
      }
    ];
    this.buttons = [
      {
        text: "保存",
        action: "save"
      },
      {
        text: "取消",
        scope: this,
        handler: this.close
      }
    ];

    this.callParent(arguments);
  }
});
```

##### (3)、修改控制器加载视图

接下来我们要做的就是在控制器加载这个视图，渲染并且加载用户信息：

```js
Ext.define('FWY.controller.Students', {
    extend: 'Ext.app.Controller',
    views: [
        'student.List',
        'student.Edit'//添加edit视图
    ],
    init: ...
    editStudent: function(grid, record) {
        var view = Ext.widget('studentedit');//注册组件，显示窗口
        view.down('form').loadRecord(record);//加载数据到表单中
    }
});
```

首先我们用 Ext.widget 方法创建了视图，这个方法等同于 `Ext.create('widget.studentedit')`，然后我们又一次借助组件查询找到了窗口中的表单，每个 ExtJS4 中的组件都有一个 `down`方法，可以借助组件查询支持的选择器来迅速找到任意下层的组件,双击表格中的一行可以看到弹窗效果。

#### 3、创建 Store 和 Model 进行重构

现在我们有了表单，可以开始编辑和保存用户信息了，但是这之前需要做一点点重构。
FWY.view.student.List 创建了一个内联的 Store ，这样可以工作但是我们需要把 Store 分离出来以便我们在应用的其他位置可以引用并更新其中的信息，我们把它放在它应该在的文件中 `app/store/Students.js` ：

```js
Ext.define("FWY.store.Students", {
  extend: "Ext.data.Store",
  fields: ["id", "name", "age", "sex"],
  data: [
    { id: 1, name: "张三", age: 30, sex: "男" },
    { id: 2, name: "李四", age: 20, sex: "女" }
  ]
});
```

现在我们需要做两处变更，首先我们需要让 Students 初始化的时候加载这个 Store ：

```js
Ext.define('FWY.controller.Students', {
    extend: 'Ext.app.Controller',
    stores: ['Students'],//加载store
    ...
});
```

然后我们要把之前直接在视图中内联的 store 更改掉，

```js
Ext.define('FWY.view.student.List' ,{
    extend: 'Ext.grid.Panel',
    alias : 'widget.studentlist',
    store: 'Students',//引用Store
    ...
});
```

控制器的代码中中引入了 store，store 会被自动加载到页面并赋予一个 storeId，这让视图中使用 store 变的容易（这个例子中，只要配置 store: 'Students' 就可以了）
现在我们只是在 store 中内联的定义了四个字段 (id,name,age,sex)，这样可以工作了。

**进一步重构：**

ExtJS4 中有一个强大的 Ext.data.Model 类，在编辑用户的时候我们可以借助它，使用 Model 重构下 Store，在 `app/model/Student.js`中创建一个 Model：

```js
Ext.define("FWY.model.Student", {
  extend: "Ext.data.Model",
  fields: ["id", "name", "age", "sex"]
});
```

这就是定义我们的 Model 需要做的，现在需要让 Store 引用 Model 替换掉使用内联字段的方式，并且让控制器也引用 Model：

```js
//修改控制器，引用Model
Ext.define('FWY.controller.Students', {
    extend: 'Ext.app.Controller',
    stores: ['Students'],
    models: ['Student'],
    ...
});
//修改store，引用Model
Ext.define('FWY.store.Students', {
    extend: 'Ext.data.Store',
    model: 'FWY.model.Student',
    data: [
        {id:1,name: '张三1',    age: 30,sex:'男'},
        {id:2,name: '李四1',    age: 21,sex:'女'}
    ]
});
```

#### 4、利用模型保存数据

现在我们有了一个用户数据表，双击每⼀一行都能打开一个编辑窗口，现在要做的是保存编辑变更，编辑窗口有一个编辑表单，还有保存按钮，现在我们更新一下控制器让保存按钮有响应：

```js
Ext.define("FWY.controller.Students", {
  init: function() {
    this.control({
      "viewport > studentlist": {
        itemdblclick: this.editStudent
      },
      "studentedit button[action=save]": {
        //获取studentedit视图中的button配置action=‘save’的按钮事件
        click: this.updateStudent
      }
    });
  },
  updateStudent: function(button) {
    console.log("clicked the Save button");
  }
});
```

接下来填充 updateStudent 真正的逻辑。我们需要把数据从表单中取出，再
设置回 store 中：

```js
updateStudent: function(button) {
    var win    = button.up('window'),
    form   = win.down('form'),
    record = form.getRecord(),
    values = form.getValues();
    record.set(values);
    win.close();
}
```

#### 5、保存到服务器

让我们增加和服务器端的交互完成这个例子。现在我们还是应编码了两行表格的数
据，现在让我们通过 ajax 加载：

```js
Ext.define("FWY.store.Students", {
  extend: "Ext.data.Store",
  model: "FWY.model.Student",
  autoLoad: true,
  proxy: {
    type: "ajax",
    url: "data/students.json",
    reader: {
      type: "json",
      root: "students",
      successProperty: "success"
    }
  }
});
```

这里我们去除了 'data' 属性，替换成 proxy ，代理是让 Store 或者 Model 加载和保存数据的一个方式，有 AJAX，JSONP，HTML5 的 localStorage 本地存储等。这里我们使用了一个简单的 AJAX 代理，让它通过 URL 'data/students.json' 加载数据。

我们同时给代理附加了一个 reader，reader 是用来把服务器返回的数据解码成 Store 能理解的格式，这次我们使用了 JSON reader，并且指定了 root 和 successProperty 配置（JSON reader 的详细配置看文档），最后我们创建一下数据文件 `data/students.json` ，输入内容：

```js
{
    success: true,
    users: [
        {id: 1, name: 'zhang',    email: 'zhang@126.com'},
        {id: 2, name: 'lishi', email: 'lishi@126.com'}
　　]
}
```

其他的变更就是我们给 Store 设置了 autoLoad 属性并设置为 true ，这意味着 Store 生成之后会自动让 Proxy 加载数据，刷新⼀一下页面应该是看到和之前同样的结果，不同的是现在不是在程序中存在硬编码数据了，最后的事情是将变更传回服务器端，这个例子中我们使用静态的 JSON 文件，没有使用数据库，但足够说明我们例子的了，首先做一点点变化告知 proxy 用于更新的 url：

```js
proxy: {
    type: 'ajax',
    api: {
        read: 'data/students.json',
        up---
date: 'data/updateStudents.json',
    },
    reader: {
        type: 'json',
        root: 'students',
        successProperty: 'success'
    }
}
```

依然从 students.json 读取数据，但是变更会发送到 updateStudents.json ，这里我们做⼀个模拟的应答回包以让我们知道程序可以正确工作， updateStudents.json 只需要包含`{"success":true}`，其他要做的就是让 Store 在编辑之后进行同步，需要在 updateStudent 函数中增加一行代码：

```js
    updateStudent: function(button) {
    var win    = button.up('window'),
    form   = win.down('form'),
    record = form.getRecord(),
    values = form.getValues();
    record.set(values);
    win.close();
    this.getStudentsStore().sync();//将数据同步到store中
}
```

最后附上本篇的代码：[点击下载]({{root_url}}/attach/ExtJs-MVC.zip)

--本篇完--
