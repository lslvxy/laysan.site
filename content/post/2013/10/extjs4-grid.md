---
title:  ExtJs4之Grid组件
date: 2013-11-17
comments: on
categories: [ExtJs]
tags: [extjs, grid,表格]
id: 201310170930
---

grid表格是extjs的核心组件之一，它提供了展示大量数据的最佳途径。Grid组件的重要特性包括：智能渲染、标准布局、数据视图、特性支持、虚拟滚动和编辑改进，这些特性共同缔造了功能强大的4.0grid组件。
<!-- more -->

**智能渲染**：在extjs4.0之前的版本中采用了"最小公分母"的策略来支持各种丰富的特性，这种方式会对每一个表格产生大量的标签，而这些标签对于简单表格来说是不必要的，而在4.0中默认的表格只会产生很少的标签，对于复杂的功能采用附加特性的方式实现，这对于提高数据的展示速度和表格的性能起到了巨大的作用。

**标准布局**：在ExtJs4.0中改变了原来直接处理内部标签和样式的布局方式，而是将表格划分为不同的组成部分，并使他们有机结合起来，这样就统一了表格和框架的渲染流程。

**数据视图**：在ExtJs4.0中新的gridView扩展自标准的DataView数据视图，这不但减少了代码冗余并且可以更简单的进行自定义。

**特性支持**：在ExtJs4.0之前的版本可以通过插件或者继承的方式对表格组件的功能进行扩展，但是这种扩展方式很难实现功能的灵活组合。4.0中使用了性的Grid基类Ext.grid.Feature，它提供了灵活定义表格特性的基础，任何Feature类都可以修改表格模版，来装饰或改变grid视图生成的标签。在新的grid类中RowWrap、RowBody和Grouping都是通过Feature方式实现的。

**虚拟滚动**：在ExtJs4.0中原生支持了渲染时数据的缓存，提供了一个虚拟的按需加载的数据视图，grid现在可以非常容易地支持几百条甚至几千条数据展示而不需要分页，这大大改进了grid的数据处理能力。

**编辑改进**：在ExtJs4.0之前的版本中开发者不得不使用editGrid类来支持表格的编辑功能，这很大程度上限制了程序的灵活性，在ExtJs4.0中提供了全新的编辑插件，它可以应用于任何grid实例。

## 1、表格面板grid

grid表格组件实在客户端展示大量数据的优秀途径，可以看作一个增强版的table，它使得获取、排序、过滤、分组、数据变得异常简单。

grid中主要集成了两大部分，分别是用于处理数据的Store和用于渲染的Columns。

下面一个简单的示例最简单的表格配置

```js
Ext.onReady(function(){
        //创建表格数据
        var datas = [
            [100,'张三',24],
            [200,'李四',30],
            [300,'王五',29]
        ];
        //创建Grid表格组件
        Ext.create('Ext.grid.Panel',{
            title : '简单Grid表格示例',
            renderTo: Ext.getBody(),
            width:200,
            height:130,
            frame:true,
            viewConfig: {
                forceFit : true,
                stripeRows: true//在表格中显示斑马线
            },
            store: {//配置数据源
                fields: ['id','name','age'],//定义字段
                proxy: {
                    type: 'memory',//Ext.data.proxy.Memory内存代理
                    data : datas,//读取内嵌数据
                    reader : 'array'//Ext.data.reader.Array解析器
                },
                autoLoad: true//自动加载
            },
            columns: [//配置表格列
                {header: "id", width: 30, dataIndex: 'id', sortable: true},
                {header: "姓名", width: 80, dataIndex: 'name', sortable: true},
                {header: "年龄", width: 80, dataIndex: 'age', sortable: true}
            ]
        });
    });
```

表格组件的主要配置项和方法如下表所示

表1-1 Ext.grid.Panel主要配置项




|配置项|参数类型|说明|
|:---|---|---|
|columns|Array|一个表格列配置对象的数组，每一个列配置对象都包括了header（列头）和数据来源的定义|
|columnLines|Boolean|设置为true则显示纵向表格线，默认为false|
|forceFit|Boolean|设置为true则强制列填充满可以利用的空间|
|hideHeaders|Boolean|设置为true则隐藏列标题|
|scroll|String/Boolean|设置表格滚动条，有效值包括both(垂直和水平滚动),horizontal(水平滚动)和vertical(垂直滚动).true等效于both,false等效none,默认值为true.|
|scrollDelta|Number|设置鼠标滚轮滚动事的像素量，默认为40像素|
|sorttableColumns|Boolean|设置为false则禁止通过表格中标题中的菜单项排序|

表1-1 Ext.grid.Panel主要方法

|方法名|说明|
|:---|---|
|getSelectionModel:Ext.selection.Model|获取选择模式|
|getStore:Ext.data.Store|获取表格的数据集|
|getView:Ext.view.Table|获取表格的视图对象|
|hideHorzontalScroller:void|隐藏水平滚动条|
|hideVerticalScroller:void|隐藏垂直滚动条|
|scrollByDeltaX(Number deltaX):void|水平滚动表格,正数向右滚动,负数向左滚动,deltaX为滚动像素|
|scrollByDeltaY(Number deltaY):void|垂直向下滚动,deltaY为滚动像素|
|setScrollTop(Number deltaY):void|垂直向上滚动,deltaY为滚动像素|
|showHorzontalScroller:void|显示水平滚动条|
|showVerticalScroller:void|显示垂直滚动条|

## 2、表格列Column

Ext.grid.column.Column类定义了表格内部与列相关的配置，其中包括列标题和数据展示的相关内容，下表中列出了该类的主要配置项

表2-1Ext.grid.column.Column主要配置项

|配置项|参数类型|说明|
|:---|---|---|
|align|String|设置列标题和数据的对齐方式，默认为left|
|columns|Array|设置组列，数组中的列将作为一组处理，组列不能排序但是可以隐藏和移动，组内的列可以移出组外，当所有的子列都被移出后组列将被自动销毁|
|dataIndex|String|设置列与数据集中的数据对应关系，值为数据模型中的字段名称|
|draggable|Boolean|设置列头是否可以移动，默认为true|
|flex|Number|设置列宽占所有flex和的比例|
|groupable|Boolean|设置在使用Ext.grid.feature.Grouping分组特性的情况下是否禁用该列在标题菜单中的分组功能|
|header|String|设置列标题|
|hideable|Boolean|设置为false则阻止用户隐藏该列，默认为true|
|menuDisabled|Boolean|设置为true则禁用标题菜单，默认为fakse|
|renderer|Function|设置列的自定义渲染函数|
|sortable|Boolean|设置是否允许进行排序，默认为true，它将根据Ext.data.Store.remoteSort判断进行本地排序还是远程排序|
|text|String|设置列标题，header配置优先|
|width|Number|设置列宽|

Column类有7个便利子类，为常用的数据类型提供了便利的展示方式，他们分别是：

Ext.grid.column.Boolean 布尔列

Ext.grid.column.Number 数字列

Ext.grid.column.Action 动作列

Ext.grid.column.Template 模版列

Ext.grid.RowNumber 行号列

Ext.tree.Column 树结构列（后面介绍）

### 2.1 布尔列Ext.grid.column.Boolean

Ext.grid.column.Boolean 定义了在表格列中显示布尔值的方式

表2-2 Ext.grid.column.Boolean只要配置项

|配置项|参数类型|说明|
|:---|---|---|
|falseText|String|设置渲染false值对应的文本，默认为false|
|trueText|String|设置渲染true值对应的文本，默认为true|
|undefinedText|String|设置渲染undefined值对应的文本，默认为空字符串|

### 2.2 数字列Ext.grid.column.Number

Ext.grid.column.Number 定义了在表格中展示数字值的方式。

配置项format，参数类型String，设置Ext.util.Format.number函数格式化字符串，默认为0，000.00

### 2.3 日期列Ext.grid.column.Date

format String 设置Date.format函数的格式化字符串，默认为Ext.data.defaultFormat

示例代码：

```js
   Ext.onReady(function(){
    //创建表格数据
    var datas = [
        ['张三',true,new Date(1979,09,13),2500],
        ['李四',false,new Date(1978,10,01),1500],
        ['王五',false,new Date(1981,01,01),1000]
    ];
    //创建Grid表格组件
    Ext.create('Ext.grid.Panel',{
        title : 'Ext.grid.column.Column示例',
        renderTo: Ext.getBody(),
        width:300,
        height:150,
        frame:true,
        store: {
            fields: ['name','leader','birthday','salary'],
            proxy: {
                type: 'memory',
                data : datas,
                reader : 'array'//Ext.data.reader.Array解析器
            },
            autoLoad: true
        },
        columns: [//配置表格列
            {header: "姓名", width: 50, dataIndex: 'name'},
            {header: "组长", width: 50, dataIndex: 'leader',
                xtype: 'booleancolumn',//Ext.grid.column.Boolean布尔列
                trueText: '是',
                falseText: '否'
            },
            {header: "生日", width: 100, dataIndex: 'birthday',
                xtype : 'datecolumn',//Ext.grid.column.Date日期列
                format : 'Y年m月d日'//日期格式化字符串
            },
            {header: "薪资", width: 50, dataIndex: 'salary',
                xtype: 'numbercolumn',//Ext.grid.column.Number数字列
                format:'0,000'//数字格式化字符串
            }
        ]
    });
});
```

### 2.4 动作列 Ext.grid.column.Action

Ext.grid.column.Action 将渲染一个图标或一系列图标到表格的单元格中，并为每一个图标创建响应函数。

|配置项|参数类型|说明|
|:---|---|---|
|altText|String|设置应用于image元素上的alt属性，默认为空字符串|
|getClass|Function|设置返回图标样式的函数|
|handler|Function|设置图标点击事件的响应函数，该函数将被传入以下参数：view：TableView 表格视图 ,rowIndex：Number 行索引 ,colIndex:Number 列索引 ,item：Object 条目 ,e：Event点击事件对象|
|icon|String|获取图标资源的url地址，默认为Ext.BLANK_IMAGE_URL|
|iconCls|String|设置应用于图标的样式|
|items|Array|包含多个图标定义的数组|
|scope|Object|设置handler和getClass函数的作用域，默认为Column|
|stopSelection|Boolean|默认为true阻止当动作发生时，当前行被选中|
|tooltip|String|设置工具提示信息，需要初始化Ext.tip.QuickTipManager|

示例代码

```js
    {header: "操作", width: 70,
    xtype: 'actioncolumn',//Ext.grid.column.Action动作列
    items: [{
        icon: 'images/edit.gif',//指定编辑图标资源的URL
        handler: function(grid, rowIndex, colIndex) {
            //获取被操作的数据记录
            var rec = grid.getStore().getAt(rowIndex);
            alert("编辑 " + rec.get('name'));
        }
    },{
        icon: 'images/del.gif',//指定编辑图标资源的URL
        handler: function(grid, rowIndex, colIndex) {
            var rec = grid.getStore().getAt(rowIndex);
            alert("删除 " + rec.get('name'));
        }                
    },{
        icon: 'images/save.gif',//指定编辑图标资源的URL
        handler: function(grid, rowIndex, colIndex) {
            var rec = grid.getStore().getAt(rowIndex);
            alert("保存 " + rec.get('name'));
        }                
    }]

}
```

### 2.5 模板列 Ext.grid.column.Template

Ext.grid.column.Template提供了通过模版渲染单元格内容的方式

tpl String/XTemplate 设置一个XTemplate模版对象或模版定义，模版数据将被传入其中

```js
{
    header: "描述", width: 100,
    xtype: 'templatecolumn',//Ext.grid.column.Template数字列
    tpl : '{name}<tpl if="leader == false">不</tpl>是组长'
}
```

### 2.6 行号列 Ext.grid.RowNumber

text String 设置显示在标题中的文本或html代码段，默认值为&#160

width Number 设置行号列的宽度，默认为23像素

### 2.7 自定义渲染函数

单元格渲染函数renderer是表格列的一项重要内容，可用来处理表格中的原始值，并将格式化后的结果返回，返回值决定了数据在单元格中的表现形式。灵活使用该函数可以实现个性化的数据展示效果。传入自定义渲染函数的参数有：

value：Mixed 当前单元格的值

metadata：Object 包含当前单元格信息的数据对象，由于设置单元格的样式和属性，该对象包含的属性有：

> tdCls：String 应用到单元格TD元素上的样式名称
>
> tdAttr： String 一个html属性定义字符串
>
> style：String 应用到单元格TD元素上的样式字符串

record：Ext.data.Model 当前数据记录对象，其中包含了与该单元格处于同一行的其他列的数据。

rowIndex： Number 当前单元格的行索引

colInde： Number 列索引

store ：Ext.data.Store 包含表格所有数据的数据集对象

view：Ext.view.View 当前的表格视图。

## 3、选择模式Selection

选择模式用来处理数据视图中记录的选择状态，Ext.selection.Model是选择模式的基类，它的子类包括Ext.selection.CellModel（单元格选择模式），Ext.selection.CheckboxModel（复选框选择模式）和Ext.selection.RowModel（行选择模式）。

### 3.1 选择模式Ext.selection.Model

Ext.selection.Model是选择模式的基类，它定义了子类需要实现的接口，这个类不能直接被创建。

表3-1 Ext.selection.Model主要配置项

|配置项|参数类型|说明|
|:---|---|---|
|allowDeselect|Boolean|设置是否允许用户在数据视图中执行撤选操作，该配置只在single单选模式下生效，默认为false|
|mode|String|设置选择模式，有效值包括 SINGLE 单选，SIMPLE简单选择和MULTI多选，默认为SINGLE单选|

表3-2 Ext.selection.Model 主要方法

|方法名|说明|
|:---|---|
|delslect(Ext.data.Model/Index records,Boolean supressEvent):void|执行撤选操作，records 数据记录或索引的数组，suppressEvent 是否抑制select事件|
|getLastSelected : Object|获取最近选择的记录数组|
|getSelection: Array|获取当前选中的记录数组|
|getSleectionMode: String|获取当前的选择模式|
|hasSelect: Boolean|获取是否有记录在被选择的状态|
|isFocused(Object rec):void|检查指定记录是否为最近选中的记录|
|isLocked(): Boolean|取得当前选择区域是否被锁定|
|isSelected(Record/Number record): Boolean|检查指定记录是否被选中|
|select(Model/Index records ,Boolean keepExiting ,Boolean suppressEvent) : void|选中记录 records 数据记录或索引的数组，keepExisting 保持，suppressEvent 是否抑制select事件|
|selectRange(Model/Number startRow,Model/Number endRow , [Boolean keepExisting],Object dir): void|选择范围内的所有行，startRow 开始索引，endRow 结束索引，keepExisting： true表示保持已有的选择，false则取消已有的选择|
|setLocked(Boolean locaked) : void|设置是否锁定当前的选择状态，locked：true表示锁定，false解锁|

### 3.2 单元格选择模式 Ext.selection.CellModel

Ext.selection.CellModel是一个简单的选择模式，用于选择表格中的单一单元格。

getCurrentPosition(): Object 得到当前选择的单元格，如果没有选择单元格则返回null

selectByPosition(pos) :void 选中指定位置的单元格，pos为位置信息，格式为{row:2,column:2}

### 3.3 行选择模式 Ext.selection.RowModel

表3-3 Ext.selection.RowModel主要配置项

|配置项|参数类型|说明|
|:---|---|---|
|enableKeyNav|Boolean|设置是否启用键盘导航，默认为true|
|simpleSelect|Boolean|设置在行选择模式下是否启用简单选择模式，如果启用则不需要按下crtl键只需通过鼠标点击就可以实现多选|
|multiSelect|Boolean|设置在行选择模式下是否支持多选|

示例代码：

```js
simpleSelect : true,//启用简单选择功能
multiSelect : true,//支持多选
selType: 'rowmodel',//设置为单元格选择模式Ext.selection.RowModel
tbar : [{
    text : '取得所选行',
    handler : function(){
        var msg = '';
        var rows = grid.getSelectionModel().getSelection();
        for(var i = 0; i < rows.length; i++){
            msg = msg + rows[i].get('name') + '\n';
        }
        alert(msg);
    }
}]
```

### 3.4 复选框选择模式 Ext.selection.CheckboxModel

Ext.selection.CheckboxModel扩展自Ext.selection.RowModel 其配置项如下;

checkOnly Boolean 设置为true则只能通过点击checkbox列进行选择，默认为false

injectCheckbox Mixed 设置注入复选框的位置，有效值可以是一个数字，false，会字符串first，last，默认为0

需要注意的是，Ext.selection.CheckboxModel没有注册selection命名空间下的别名，导致不能直接使用，因此需要编写别名注册代码，示例如下：

```js
//注册复选框选择模式别名为selection.checkboxmodel
Ext.ClassManager.setAlias('Ext.selection.CheckboxModel','selection.checkboxmodel');
multiSelect : true,//支持多选
selModel: {
    elType : 'checkboxmodel'//复选框选择模式Ext.selection.CheckboxModel
}
```

## 4、表格特性 Feature

Ext.grid.feature.Feature是一类针对Ext.grid.Panel的特殊插件，它提供了一些扩展点。其子类包括：

Ext.grid.feature.RowBody 表格行体

Ext.grid.feature.Summary 表格汇总

Ext.grid.feature.Grouping 表格分组

Ext.grid.feature.GroupingSummary 分组汇总

### 4.1 表格行体 Ext.grid.feature.RowBody

行体特性为表格追加了tr标签，它跨越了原始表格的所有列。该特性在表格中展示一些描述性的特殊信息时非常有用，行体在默认状态下是隐藏的，如果需要展示行体必须覆盖geyAdditionalData方法。

使用行体会自动在表格视图中暴露已rowbody为前缀的事件，示例如下：

```js
features: [Ext.create('Ext.grid.feature.RowBody',{
    getAdditionalData: function(data, idx, record, orig) {
        var headerCt = this.view.headerCt,
            colspan  = headerCt.getColumnCount();//获取表格的列数

        return {
            rowBody: record.get('introduce'),//指定行体内容
            rowBodyCls: 'rowbodyColor',//指定行体样式
            rowBodyColspan: colspan//指定行体跨列的列数
        };
    }
})]
```

### 4.2 表格汇总 Ext.grid.feature.Summary

表格汇总特性将在表格的底部显示一个汇总行，关于汇总行有2点需要注意：

1、汇总值的计算，汇总值需要根据表格的每一列进行计算，计算方式通过column中的summaryType配置项进行指定，内置的汇总计算类型包括：count 计数；sum 求和；min 最小值；max 最大值；average 平均值。

2、汇总值的渲染，与column的渲染方式相同，汇总值的渲染支持summaryRenderer函数，该函数是可选的，传入函数的参数有：

value{Object}:合计值

data{Objject}:包含所有合计值的行数据

field{String}:进行求和计算的字段名

示例代码：

```js
Ext.onReady(function(){
        //创建表格数据
        var datas = [
            ['张三',2500],
            ['李四',1500]
        ];
        //创建Grid表格组件
        Ext.create('Ext.grid.Panel',{
            title : 'Ext.grid.feature.Summary示例',
            renderTo: Ext.getBody(),
            width:300,
            height:150,
            frame:true,
            store: {
                fields: ['name','salary','introduce'],
                proxy: {
                    type: 'memory',
                    data : datas,
                    reader : 'array'//Ext.data.reader.Array解析器
                },
                autoLoad: true
            },
            features: [{
                ftype: 'summary'//Ext.grid.feature.Summary表格汇总特性
            }],
            columns: [//配置表格列
                {header: "姓名", flex: 1, dataIndex: 'name',
                    summaryType: 'count',//求数量
                    summaryRenderer: function(value){
                        return '员工总数：'+value
                    }
                },
                {header: "薪资", flex: 1, dataIndex: 'salary',
                    summaryType: 'average',//求平均值
                    summaryRenderer: function(value){
                        return '平均薪资：'+value
                    }
                }
            ]
        });
    });
```

### 4.3 表格分组 Ext.grid.feature.Grouping

表格分组特性将表格按照分组的方式进行聚合展示，在每一个分组标题之下展示与之匹配的数据记录，分组之后的数据可以展开或收缩，该特性有以下3点需要注意的地方：

**新增事件**：包括 groupclick、groupdblclick、groupcontextmenu、groupexpand、groupcollapse。

**标题栏扩展**：标题菜单中会增加分组相关功能，通过enableGroupingMenu配置项来控制该功能是否启用。

**定义分组标题**：功过groupHeaderTpl可以定义分组标题显示模版。

表4-1Ext.grid.feature.Grouping 主要配置项

|配置项|参数类型|说明|
|:---|:---|---|
|depthToIndent|Number|设置分组数据的缩进，默认为17像素|
|enableGroupingMenu|Boolean|设置是否启用标题菜单中的分组功能，默认为true|
|enableNoGroups|Boolean|设置是否允许用户关闭分组，默认为true|
|groupByText|String|设置显示在分组菜单中的分组功能名称，默认为group By This Field|
|groupHeaderTpl|String|设置分组标题模板，默认为Group:{name}|
|hideGroupedHeader|Boolean|设置是否隐藏分组标题，默认为false|
|showGroupsText|String|设置标题菜单中是否分组显示文字说明，默认为 show in groups|
|startCollapsed|Boolean|设置分组是否默认收缩，默认为false|

示例代码：

```js
Ext.onReady(function(){
        //创建表格数据
        var datas = [
            ['张三','男',29],['李四','女',30],
            ['王五','男',27],['赵六','女',31]
        ];
        //创建Grid表格组件
        Ext.create('Ext.grid.Panel',{
            title : 'Ext.grid.feature.Grouping示例',
            renderTo: Ext.getBody(),
            width:300,
            height:150,
            frame:true,
            store: {
                fields: ['name','sex','age'],
                groupField: 'sex',//设置分组字段
                proxy: {
                    type: 'memory',
                    data : datas,
                    reader : 'array'//Ext.data.reader.Array解析器
                },
                autoLoad: true
            },
            features: [Ext.create('Ext.grid.feature.Grouping', {
                groupByText : '用本字段分组',
                showGroupsText : '显示分组',
                groupHeaderTpl: '性别: {name} ({rows.length})', //分组标题模版
                startCollapsed: true //设置初始分组是否收起
            })],
            columns: [//配置表格列
                {header: "姓名", flex: 1, dataIndex: 'name'},
                {header: "性别", flex: 1, dataIndex: 'sex'},
                {header: "年龄", flex: 1, dataIndex: 'age'}
            ]
        });
    });
```

### 4.4 分组汇总 Ext.grid.feature.GroupingSummary

分组汇总特性结合了Grouping分组和summary汇总两个特性的特点，它在每一个分组下增加一行显示汇总数据，其相关配置可以参考Grouping和summary的配置项。

## 5、表格插件plugin

为了扩展表格组件已有功能，除了前面介绍的特性之外，extjs还提供了表格的扩展插件，通过插件实现表格的编辑，拖拽等功能。

单元格编辑插件：Ext.grid.plugin.CellEditing

行编辑插件：Ext.grid.plugin.RowEditing

拖拽插件： Ext.grid.plugin.DragDrop

### 5.1 单元格编辑插件 Ext.grid.plugin.CellEditing

Ext.grid.plugin.CellEditing插件为grid组件注入了单元格级别的编辑功能，同一时间只能有一个单元格处于编辑状态，表单字段作为编辑器，如果表格中的某列没有指定编辑器则该列不能被编辑。其主要配置项如下：

clicksToEdit Number 设置点击单元格进入编辑模式的点击次数，默认为2

示例代码如下：

```js
Ext.onReady(function(){
        //初始化提示信息
        Ext.QuickTips.init();
        //创建表格数据
        var datas = [
            ['张三',new Date(1979,09,13),2500],
            ['李四',new Date(1978,10,01),1500],
            ['王五',new Date(1981,01,01),1000]
        ];
        //创建Grid表格组件
        Ext.create('Ext.grid.Panel',{
            title : 'Ext.grid.plugin.CellEditing示例',
            renderTo: Ext.getBody(),
            width:300,
            height:150,
            frame:true,
            store: {
                fields: ['name','birthday','salary'],
                proxy: {
                    type: 'memory',
                    data : datas,
                    reader : 'array'//Ext.data.reader.Array解析器
                },
                autoLoad: true
            },
            plugins: [
                Ext.create('Ext.grid.plugin.CellEditing', {
                    clicksToEdit: 1//设置鼠标单击1次进入编辑状态
                })
            ],
            selType: 'cellmodel',//设置为单元格选择模式
            columns: [//配置表格列
              Ext.create('Ext.grid.RowNumberer',{text : '行号', width : 35}),
              {header: "姓名", width: 50, dataIndex: 'name',
                    editor: {//文本字段
                        xtype:'textfield',
                        allowBlank:false
                    }
                },
                {header: "生日", width: 100, dataIndex: 'birthday',
                    xtype : 'datecolumn',//Ext.grid.column.Date日期列
                    format : 'Y年m月d日',//日期格式化字符串
                    editor: {//日期字段
                        xtype:'datefield',
                        allowBlank:false
                    }
                },
                {header: "薪资", width: 50, dataIndex: 'salary',
                    xtype: 'numbercolumn',//Ext.grid.column.Number数字列
                    format:'0,000',//数字格式化字符串
                    editor: {//数字字段
                        xtype:'numberfield',
                        allowBlank:false
                    }
                }
            ]
        });
    });
```

保存编辑后的数据有2中基本方式

1.监听表格的edit事件，在每一次编辑后该事件都会触发，在事件处理函数中奖修改后的数据保存到服务器中，例如：

```js
grid.on('edit',onEdit,this);
function onEdit(e){
    //执行ajax请求将数据提交至服务器
    e.record.commit();
};
```

2、建立单独的数据保存处理函数，该函数有用户决定何时触发，在函数中获取所有修改过的表格数据，一次性将多条修改后的数据同步到服务器。

### 5.2 行编辑插件：Ext.grid.plugin.RowEditing

Ext.grid.plugin.RowEditing为grid组件注入了行级别的编辑功能，编辑开始时会显示一个小的浮动面板，每一个配置了编辑器的表格列都将以字段的形式显示在面板上，没有配置编辑器的列将以文本的形式显示在面板中。其配置项有

autoCancel Boolean 设置在切换所编辑的行时是否自动取消任何未确定的数据修改，默认为true。

clicksToMoveEditor Number 设置编辑器移动到新行鼠标需要点击的次数，默认同clicksToEdit的值一致

errorSummary Boolean 设置是否显示一个展开所有字段验证信息的工具提示，默认为true

修改上节的代码，将编辑器模式切换为行编辑模式。

```js
plugins: [
//行编辑模式
Ext.create('Ext.grid.plugin.RowEditing', {
clicksToEdit: 1
})
]
```

### 5.3 拖拽插件： Ext.grid.plugin.DragDrop

Ext.grid.plugin.DragDrop 插件为表格视图提供了拖放功能，它自动创建了特殊的DragZone和Ext.dd.DropZone实例来协作完成拖放功能。

ddGroup String 设置拖放组名称，拖放操作只能在相同的组内进行，默认为TreeDD

dragGroop String 设置拖拽组名称

dropGroup String 设置释放组名称

enableDrag Boolean 设置是否启用拖动功能，默认为true

enableDrop Boolean 设置是否启用释放功能，默认为true

示例代码：

grid1：

```js
viewConfig: {
plugins: [
    //行编辑模式
    Ext.create('Ext.grid.plugin.DragDrop',{
        dragGroup: 'grid1',//拖拽组名称
        dropGroup: 'grid2'//拖放组名称
    })
]
}
```

grid2：

```js
viewConfig: {
plugins: [
    //行编辑模式
    Ext.create('Ext.grid.plugin.DragDrop',{
        dragGroup: 'grid2',//拖拽组名称
        dropGroup: 'grid1'//拖放组名称
    })
]
}
```

## 6、表格分页

当表格数据量比较大时，对数据进行分页显示是常见的处理方法，在extjs中分页只需要引入分业工具栏Ext.toolbar.Paging就可以实现基本的分页功能。示例如下：

```js
Ext.onReady(function(){
        var itemsPerPage = 2;//指定分页大小

        var store = Ext.create('Ext.data.Store', {
            autoLoad: {start: 0, limit: itemsPerPage},
            fields:['id', 'name', 'age'],
            pageSize: itemsPerPage, //设置分页大小
            proxy: {
                type: 'ajax',
                url: 'jsonServer.jsp',  //请求的服务器地址
                reader: {
                    type: 'json',
                    root: 'rows',
                    totalProperty: 'results'
                }
            }
        });
        //创建Grid表格组件
        Ext.create('Ext.grid.Panel',{
            title : 'Ext.toolbar.Paging示例',
            renderTo: Ext.getBody(),
            width:400,
            height:150,
            frame:true,
            store: store,
            columns: [//配置表格列
                {header: "id", width: 30, dataIndex: 'id', sortable: true},
                {header: "姓名", width: 80, dataIndex: 'name', sortable: true},
                {header: "年龄", width: 80, dataIndex: 'age', sortable: true}
            ],
            bbar: [{
                xtype: 'pagingtoolbar',
                store: store,   //这里需要指定与表格相同的store
                displayInfo: true，
                displayMsg: '显示第 {0} 条到 {1} 条记录，一共 {2} 条',
         emptyMsg: "当前查询条件无数据,请重新查询"

            }]
        });
    });
```

服务器端返回的数据格式为:

`{results:6,rows:[{id:0,name:'tom',age:24},{id:1,name:'jack',age:18}]}`

最后附上本篇的源代码：[点击这里下载]({{root_url}}/attach/Extjs-grid.zip)
