drop table `rap_playlist163`;
CREATE TABLE `rap_playlist163` (
`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`title` varchar(150) NOT NULL DEFAULT '' COMMENT '标题',
`link` varchar(120) NOT NULL DEFAULT '' COMMENT '链接',
`play_num` varchar(20) NOT NULL DEFAULT '0' COMMENT '播放量',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`status` int(4) NOT NULL DEFAULT '0' COMMENT '歌单状态（0：未生成歌曲，1：生成歌曲中，2：已生成歌曲）',
PRIMARY KEY (`id`),
UNIQUE KEY `link` (`link`),
KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='歌单表';


-- drop table `rap_music163`;
CREATE TABLE `rap_music163` (
`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`song_id` int(11) NOT NULL DEFAULT '0' COMMENT '歌曲id',
`name` varchar(200) NOT NULL DEFAULT ''  COMMENT '歌曲名称',
`link` varchar(120) NOT NULL DEFAULT '' COMMENT '链接',
`lyric` MediumText NOT NULL COMMENT '歌词',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`status` int(4) NOT NULL DEFAULT '0' COMMENT '歌单状态（0：未获取歌曲详细内容（如歌词），1：已获取歌曲详细内容，2：分词中，3：已分词）',
PRIMARY KEY (`id`),
UNIQUE KEY `link` (`link`),
KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='歌曲表';


drop table `rap_word163`;
CREATE TABLE `rap_word163` (
`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`word` varchar(20) NOT NULL DEFAULT ''  COMMENT '词',
`count` int(11) NOT NULL DEFAULT '0' COMMENT '词出现次数',
`pinyin` varchar(30) NOT NULL DEFAULT ''  COMMENT '词对应拼音',
`rhyme` varchar(30) NOT NULL DEFAULT ''  COMMENT '韵脚',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`status` int(4) NOT NULL DEFAULT '0' COMMENT '',
PRIMARY KEY (`id`),
KEY `status` (`status`),
UNIQUE KEY `word` (`word`),
KEY `rhyme` (`rhyme`),
KEY `pinyin` (`pinyin`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='分词表';

