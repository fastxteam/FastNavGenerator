#!/usr/bin/env python3
"""
导航网站生成器 - JSON 配置文件版本
支持本地文件夹打开功能、发布说明时间轴和版本接口
开发者: @wanqiang.liu
"""

import datetime
import argparse
import sys
import os
import json
from collections import defaultdict


class JavaScriptManager:
    """JavaScript 代码管理器"""

    @staticmethod
    def get_main_script():
        """获取主 JavaScript 脚本"""
        return """
        // 主初始化函数
        function initNavigation() {
            initCategoryNavigation();
            initReleaseNotes();
            initLayoutControls();
            initTagFilters();
            initLocalFolderFeatures();
            initInterfaceRoutes();
            initIconReference();
            initUsageTooltip();
            initKeyboardShortcuts();
            initNotificationSystem();
        }
        """

    @staticmethod
    def get_category_navigation_script():
        """分类导航脚本"""
        return """
        // 1. 分类导航功能
        function initCategoryNavigation() {
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.preventDefault();

                    // 移除所有active类
                    document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
                    document.querySelectorAll('.category-section').forEach(section => section.classList.remove('active'));

                    // 添加active类
                    item.classList.add('active');
                    const category = item.getAttribute('data-category');
                    document.getElementById(category).classList.add('active');
                });
            });
        }
        """

    @staticmethod
    def get_release_notes_script():
        """发布说明脚本"""
        return """
        // 2. 发布说明功能
        function initReleaseNotes() {
            // 发布类型卡片点击事件
            document.querySelectorAll('.release-type-card').forEach(card => {
                card.addEventListener('click', (e) => {
                    e.preventDefault();

                    // 移除所有active类
                    document.querySelectorAll('.release-type-card').forEach(c => c.classList.remove('active'));

                    // 添加active类
                    card.classList.add('active');

                    const releaseType = card.getAttribute('data-release-type');
                    showReleaseTimeline(releaseType);
                });
            });
        }

        // 显示发布类型时间轴
        function showReleaseTimeline(releaseType) {
            // 隐藏所有时间轴
            document.querySelectorAll('.timeline').forEach(timeline => {
                timeline.style.display = 'none';
            });

            // 显示选中的时间轴
            const targetTimeline = document.getElementById(`timeline-${releaseType}`);
            if (targetTimeline) {
                targetTimeline.style.display = 'block';
            }
        }
        """

    @staticmethod
    def get_layout_controls_script():
        """布局控制脚本"""
        return """
        // 3. 布局切换功能
        function initLayoutControls() {
            document.querySelectorAll('.layout-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const layout = this.getAttribute('data-layout');
                    const container = this.closest('.category-section').querySelector('.cards-container');
                    const buttons = this.parentElement.querySelectorAll('.layout-btn');

                    // 更新按钮状态
                    buttons.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');

                    // 切换布局
                    container.className = 'cards-container ' + layout + '-layout';
                });
            });
        }
        """

    @staticmethod
    def get_tag_filters_script():
        """标签筛选脚本"""
        return """
        // 4. 标签筛选功能
        function initTagFilters() {
            document.querySelectorAll('.tag-filter').forEach(filter => {
                filter.addEventListener('click', function() {
                    const tag = this.getAttribute('data-tag');
                    const container = this.closest('.category-section').querySelector('.cards-container');
                    const filters = this.parentElement.querySelectorAll('.tag-filter');

                    // 更新按钮状态
                    filters.forEach(f => f.classList.remove('active'));
                    this.classList.add('active');

                    // 筛选卡片
                    const cards = container.querySelectorAll('.link-card');
                    cards.forEach(card => {
                        if (tag === '全部') {
                            card.style.display = 'flex';
                        } else {
                            const cardTags = card.getAttribute('data-tags');
                            if (cardTags && cardTags.includes(tag)) {
                                card.style.display = 'flex';
                            } else {
                                card.style.display = 'none';
                            }
                        }
                    });
                });
            });
        }
        """

    @staticmethod
    def get_local_folder_script():
        """本地文件夹功能脚本"""
        return """
        // 5. 本地文件夹功能
        function initLocalFolderFeatures() {
            // 复制路径功能
            document.querySelectorAll('.copy-path-btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const path = this.getAttribute('data-path');
                    copyToClipboard(path);
                    showNotification('路径已复制到剪贴板', 'success');
                });
            });

            // 本地文件夹右键菜单
            document.querySelectorAll('.card-actions.local-folder a.local-path').forEach(link => {
                link.addEventListener('contextmenu', function(e) {
                    e.preventDefault();
                    const card = this.closest('.link-card');
                    const path = card.getAttribute('data-original-path');
                    showFolderOptions(path);
                });
            });

            // 双击卡片标题复制路径（仅限本地文件夹）
            document.querySelectorAll('.link-card[data-is-local="true"] h3').forEach(title => {
                title.addEventListener('dblclick', function() {
                    const card = this.closest('.link-card');
                    const path = card.getAttribute('data-original-path');
                    copyToClipboard(path);
                    showNotification('路径已复制到剪贴板', 'success');
                });
            });
        }
        """

    @staticmethod
    def get_interface_routes_script():
        """版本接口脚本"""
        return """
        // 6. 版本接口功能
        function initInterfaceRoutes() {
            // 视图切换功能
            document.querySelectorAll('.view-filter').forEach(filter => {
                filter.addEventListener('click', function() {
                    const view = this.getAttribute('data-view');
                    const container = this.closest('.interface-route-container');
                    const filters = container.querySelectorAll('.view-filter');

                    // 更新按钮状态
                    filters.forEach(f => f.classList.remove('active'));
                    this.classList.add('active');

                    // 切换视图内容
                    const viewContents = container.querySelectorAll('.view-content');
                    viewContents.forEach(content => {
                        if (content.getAttribute('data-view') === view) {
                            content.style.display = 'block';
                        } else {
                            content.style.display = 'none';
                        }
                    });
                });
            });

            // 分支筛选功能
            document.querySelectorAll('.branch-filter').forEach(filter => {
                filter.addEventListener('click', function() {
                    const branch = this.getAttribute('data-branch');
                    const container = this.closest('.interface-route-container');
                    const filters = container.querySelectorAll('.branch-filter');

                    // 更新按钮状态
                    filters.forEach(f => f.classList.remove('active'));
                    this.classList.add('active');

                    // 筛选表格行
                    const activeView = container.querySelector('.view-filter.active').getAttribute('data-view');
                    const tableContainer = container.querySelector(`.view-content[data-view="${activeView}"]`);

                    if (branch === 'all') {
                        // 显示所有行
                        tableContainer.querySelectorAll('tr[data-branch]').forEach(row => {
                            row.style.display = '';
                        });
                        tableContainer.querySelectorAll('.branch-group').forEach(group => {
                            group.style.display = 'block';
                        });
                    } else {
                        if (activeView === 'unified') {
                            // 统一视图：筛选行
                            tableContainer.querySelectorAll('tr[data-branch]').forEach(row => {
                                if (row.getAttribute('data-branch') === branch) {
                                    row.style.display = '';
                                } else {
                                    row.style.display = 'none';
                                }
                            });
                        } else {
                            // 分组视图：筛选分组
                            tableContainer.querySelectorAll('.branch-group').forEach(group => {
                                if (group.getAttribute('data-branch') === branch) {
                                    group.style.display = 'block';
                                } else {
                                    group.style.display = 'none';
                                }
                            });
                        }
                    }
                });
            });
        }
        """

    @staticmethod
    def get_icon_reference_script():
        """图标引用脚本"""
        return """
        // 7. 图标引用功能
        function initIconReference() {
            // 统一复制函数
            function copyIcon(value) {
                copyToClipboard(value);
                if (value.length <= 2) {
                    // 可能是emoji
                    showNotification(`Emoji已复制: ${value}`, 'success');
                } else {
                    // 可能是SVG ID
                    showNotification(`SVG图标ID已复制: ${value}`, 'success');
                }
            }

            // 修改图标项点击事件
            document.addEventListener('click', (e) => {
                const iconItem = e.target.closest('.icon-item');
                if (iconItem) {
                    if (iconItem.classList.contains('svg-item')) {
                        // SVG图标：复制ID
                        const iconId = iconItem.getAttribute('data-icon-id');
                        if (iconId) {
                            copyToClipboard(iconId);
                            showNotification(`SVG图标ID已复制: ${iconId}`, 'success');
                        }
                    } else {
                        // Emoji图标：复制emoji
                        const icon = iconItem.getAttribute('data-icon');
                        if (icon) {
                            copyToClipboard(icon);
                            showNotification(`Emoji已复制: ${icon}`, 'success');
                        }
                    }
                }
            });
        }
        """

    @staticmethod
    def get_usage_tooltip_script():
        """使用提示脚本"""
        return """
        // 8. 使用提示功能
        function initUsageTooltip() {
            // 简洁版使用说明功能
            function toggleUsageTooltip() {
                const tooltip = document.getElementById('usageTooltip');
                tooltip.classList.toggle('show');
            }

            // 绑定点击事件
            const helpBtn = document.querySelector('.usage-help');
            if (helpBtn) {
                helpBtn.addEventListener('click', toggleUsageTooltip);
            }

            // 点击页面其他地方关闭工具提示
            document.addEventListener('click', (e) => {
                const tooltip = document.getElementById('usageTooltip');
                const helpBtn = document.querySelector('.usage-help');

                if (tooltip && tooltip.classList.contains('show') && 
                    !tooltip.contains(e.target) && 
                    !helpBtn.contains(e.target)) {
                    tooltip.classList.remove('show');
                }
            });

            // ESC键关闭工具提示
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    const tooltip = document.getElementById('usageTooltip');
                    if (tooltip) {
                        tooltip.classList.remove('show');
                    }
                }
            });
        }
        """

    @staticmethod
    def get_keyboard_shortcuts_script():
        """键盘快捷键脚本"""
        return """
        // 9. 键盘快捷键功能
        function initKeyboardShortcuts() {
            document.addEventListener('keydown', (e) => {
                // Alt + 数字 切换分类
                if (e.altKey) {
                    const categories = Array.from(document.querySelectorAll('.nav-item'));
                    const index = parseInt(e.key) - 1;
                    if (index >= 0 && index < categories.length) {
                        categories[index].click();
                    }
                }

                // ESC 键关闭模态框和工具提示
                if (e.key === 'Escape') {
                    hideModal();
                    const tooltip = document.getElementById('usageTooltip');
                    if (tooltip) {
                        tooltip.classList.remove('show');
                    }
                }
            });
        }
        """

    @staticmethod
    def get_notification_system_script():
        """通知系统脚本"""
        return """
        // 10. 通知系统功能
        function initNotificationSystem() {
            // 这个函数是全局可用的，其他模块会调用它
        }

        // 工具函数：复制到剪贴板
        function copyToClipboard(text) {
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(text);
            } else {
                // 备用方法
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                try {
                    document.execCommand('copy');
                } catch (err) {
                    console.error('复制失败:', err);
                }
                document.body.removeChild(textArea);
            }
        }

        // 工具函数：显示通知
        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = 'notification ' + type;
            notification.classList.add('show');

            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }

        // 工具函数：显示文件夹选项
        function showFolderOptions(path) {
            document.getElementById('modalFolderPath').textContent = path;
            document.getElementById('folderOptionsModal').classList.add('show');
        }

        // 工具函数：隐藏模态框
        function hideModal() {
            document.getElementById('folderOptionsModal').classList.remove('show');
        }
        """

    @staticmethod
    def get_modal_script():
        """模态框功能脚本"""
        return """
        // 模态框功能
        document.getElementById('modalCopyPath').addEventListener('click', function() {
            const path = document.getElementById('modalFolderPath').textContent;
            copyToClipboard(path);
            showNotification('路径已复制到剪贴板', 'success');
            hideModal();
        });

        document.getElementById('modalOpenDefault').addEventListener('click', function() {
            const path = document.getElementById('modalFolderPath').textContent;
            // 转换为 file:// URL 并打开
            let fileUrl = path;
            if (!fileUrl.startsWith('file://')) {
                if (fileUrl.startsWith('/')) {
                    fileUrl = 'file://' + fileUrl;
                } else {
                    fileUrl = 'file:///' + fileUrl.replace(/\\\\/g, '/');
                }
            }
            window.open(fileUrl, '_blank');
            hideModal();
        });

        document.getElementById('modalCancel').addEventListener('click', hideModal);
        document.getElementById('folderOptionsModal').addEventListener('click', function(e) {
            if (e.target === this) hideModal();
        });
        """

    @staticmethod
    def get_onload_script():
        """页面加载后执行的脚本"""
        return """
        // 页面加载完成后初始化所有功能
        document.addEventListener('DOMContentLoaded', function() {
            // 初始化所有功能模块
            initNavigation();

            // 绑定模态框事件（确保在DOM加载后）
            const modalCopyBtn = document.getElementById('modalCopyPath');
            const modalOpenBtn = document.getElementById('modalOpenDefault');
            const modalCancelBtn = document.getElementById('modalCancel');
            const modalOverlay = document.getElementById('folderOptionsModal');

            if (modalCopyBtn) {
                modalCopyBtn.addEventListener('click', function() {
                    const path = document.getElementById('modalFolderPath').textContent;
                    copyToClipboard(path);
                    showNotification('路径已复制到剪贴板', 'success');
                    hideModal();
                });
            }

            if (modalOpenBtn) {
                modalOpenBtn.addEventListener('click', function() {
                    const path = document.getElementById('modalFolderPath').textContent;
                    let fileUrl = path;
                    if (!fileUrl.startsWith('file://')) {
                        if (fileUrl.startsWith('/')) {
                            fileUrl = 'file://' + fileUrl;
                        } else {
                            fileUrl = 'file:///' + fileUrl.replace(/\\\\/g, '/');
                        }
                    }
                    window.open(fileUrl, '_blank');
                    hideModal();
                });
            }

            if (modalCancelBtn) {
                modalCancelBtn.addEventListener('click', hideModal);
            }

            if (modalOverlay) {
                modalOverlay.addEventListener('click', function(e) {
                    if (e.target === this) hideModal();
                });
            }

            // 绑定使用提示按钮
            const helpBtn = document.querySelector('.usage-help');
            if (helpBtn) {
                helpBtn.addEventListener('click', function() {
                    const tooltip = document.getElementById('usageTooltip');
                    if (tooltip) {
                        tooltip.classList.toggle('show');
                    }
                });
            }
        });
        """

    @staticmethod
    def get_all_scripts():
        """获取所有 JavaScript 脚本"""
        scripts = [
            JavaScriptManager.get_main_script(),
            JavaScriptManager.get_category_navigation_script(),
            JavaScriptManager.get_release_notes_script(),
            JavaScriptManager.get_layout_controls_script(),
            JavaScriptManager.get_tag_filters_script(),
            JavaScriptManager.get_local_folder_script(),
            JavaScriptManager.get_interface_routes_script(),
            JavaScriptManager.get_icon_reference_script(),
            JavaScriptManager.get_usage_tooltip_script(),
            JavaScriptManager.get_keyboard_shortcuts_script(),
            JavaScriptManager.get_notification_system_script(),
            JavaScriptManager.get_modal_script(),
            JavaScriptManager.get_onload_script()
        ]

        # 将所有脚本合并成一个字符串
        return "\n".join(scripts)

class CSSManager:
    """CSS样式管理器"""

    @staticmethod
    def get_base_styles():
        """基础样式"""
        return """
        :root {
            --primary-color: #6366f1;
            --primary-hover: #4f46e5;
            --bg-color: #ffffff;
            --sidebar-bg: #f8fafc;
            --card-bg: #ffffff;
            --text-primary: #374151;
            --text-secondary: #6b7280;
            --border-color: #e5e7eb;
            --shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            --shadow-hover: 0 4px 12px rgba(0, 0, 0, 0.08);
            --border-radius: 8px;
            --transition: all 0.2s ease;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --copy-btn-color: #8b5cf6;
            --copy-btn-hover: #7c3aed;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-color);
            color: var(--text-primary);
            display: flex;
            min-height: 100vh;
            line-height: 1.6;
        }

        @keyframes fadeIn {
            from { 
                opacity: 0; 
                transform: translateY(10px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        """

    @staticmethod
    def get_layout_styles():
        """布局样式"""
        return """
        /* 侧边栏样式 */
        .sidebar {
            width: 280px;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            padding: 30px 0;
            height: 100vh;
            position: fixed;
            left: 0;
            top: 0;
            overflow-y: auto;
        }

        /* 主内容区样式 */
        .main-content {
            flex: 1;
            margin-left: 280px;
            padding: 40px 60px;
            background: var(--bg-color);
            max-width: calc(100% - 280px);
            box-sizing: border-box;
        }

        .category-section {
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .category-section.active {
            display: block;
        }
        """

    @staticmethod
    def get_logo_styles():
        """Logo和导航样式"""
        return """
        .logo {
            text-align: center;
            padding: 0 25px 30px 25px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 25px;
        }

        .logo h1 {
            font-size: 1.8em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color), #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .logo p {
            color: var(--text-secondary);
            font-size: 0.9em;
        }

        .nav-categories {
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding: 0 15px;
        }

        .nav-item {
            padding: 14px 16px;
            border-radius: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: var(--transition);
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 12px;
            border: none;
            background: none;
            cursor: pointer;
            text-align: left;
            font-size: 0.95em;
            width: 100%;
        }

        .nav-item:hover {
            background: rgba(99, 102, 241, 0.08);
            color: var(--primary-color);
        }

        .nav-item.active {
            background: var(--primary-color);
            color: white;
        }

        .nav-item i {
            width: 20px;
            text-align: center;
            font-size: 1.1em;
        }
        """

    @staticmethod
    def get_section_styles():
        """分类页面样式"""
        return """
        .section-header {
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }

        .section-title h2 {
            font-size: 1.8em;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
        }

        .section-title p {
            color: var(--text-secondary);
            font-size: 1em;
        }

        /* 标签筛选器样式 */
        .tag-filters {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 20px;
            padding: 16px;
            background: var(--sidebar-bg);
            border-radius: var(--border-radius);
        }

        .tag-filter {
            padding: 6px 12px;
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 20px;
            cursor: pointer;
            transition: var(--transition);
            font-size: 0.85em;
            color: var(--text-secondary);
        }

        .tag-filter:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
        }

        .tag-filter.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }

        /* 布局切换按钮 */
        .layout-controls {
            display: flex;
            gap: 8px;
        }

        .layout-btn {
            padding: 8px 16px;
            border: 1px solid var(--border-color);
            background: white;
            border-radius: 6px;
            cursor: pointer;
            transition: var(--transition);
            font-size: 0.9em;
            color: var(--text-secondary);
        }

        .layout-btn:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
        }

        .layout-btn.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
        """

    @staticmethod
    def get_card_styles():
        """卡片和链接样式"""
        return """
        /* 列表布局 */
        .cards-container.list-layout {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(540px, 1fr));
            gap: 16px;
            width: 100%;
        }

        /* 格子布局 */
        .cards-container.grid-layout {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }

        .grid-layout .link-card {
            height: 100%;
            flex-direction: column;
            display: flex;
        }

        .grid-layout .card-content {
            flex: 1;
            padding: 20px 24px;
            display: flex;
            flex-direction: column;
        }

        .grid-layout .card-info {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .grid-layout .card-header {
            margin-bottom: 12px;
        }

        .grid-layout .description {
            flex: 1;
            margin-bottom: 0;
        }

        /* 访问按钮容器移到卡片底部 */
        .grid-layout .card-actions {
            order: 2;
            border-right: none;
            border-top: 1px solid var(--border-color);
            width: 100%;
            justify-content: center;
            background: rgba(99, 102, 241, 0.03);
            transition: var(--transition);
            margin-top: auto;
        }

        .grid-layout .card-actions:hover {
            background: rgba(99, 102, 241, 0.08);
        }

        .grid-layout .link-card a {
            padding: 14px 24px;
            width: 100%;
            justify-content: center;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .grid-layout .link-card a:hover {
            color: var(--primary-color);
            background: transparent;
        }

        /* 确保卡片内容正确排序 */
        .grid-layout .card-content {
            order: 1;
        }

        /* 确保整个卡片使用列布局 */
        .grid-layout .link-card {
            display: flex;
            flex-direction: column;
        }

        .link-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            transition: var(--transition);
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: stretch;
        }

        .link-card:hover {
            transform: translateY(-1px);
            box-shadow: var(--shadow-hover);
            border-color: var(--primary-color);
        }

        .link-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
            background: var(--primary-color);
            opacity: 0;
            transition: var(--transition);
        }

        .link-card:hover::before {
            opacity: 1;
        }

        /* 卡片操作区域 */
        .card-actions {
            display: flex;
            align-items: stretch;
            flex-shrink: 0;
            background: rgba(99, 102, 241, 0.03);
            border-right: 1px solid var(--border-color);
            transition: var(--transition);
            position: relative;
        }

        /* 标签容器 */
        .tag-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 0 8px;
            background: rgba(139, 92, 246, 0.05);
            border-right: 1px solid rgba(139, 92, 246, 0.2);
            writing-mode: vertical-rl;
            text-orientation: mixed;
            min-width: 28px;
        }

        .link-tag {
            font-size: 0.7em;
            font-weight: 600;
            color: var(--copy-btn-color);
            letter-spacing: 0.5px;
            transform: rotate(0deg);
            white-space: nowrap;
        }

        .link-card a {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            padding: 0 24px;
            background: transparent;
            color: var(--text-secondary);
            text-decoration: none;
            transition: var(--transition);
            font-weight: 500;
            font-size: 0.9em;
            white-space: nowrap;
            min-height: 100%;
        }

        .link-card a:hover {
            background: rgba(99, 102, 241, 0.08);
            color: var(--primary-color);
        }

        .card-content {
            flex: 1;
            padding: 20px 24px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 20px;
        }

        .card-info {
            flex: 1;
            min-width: 0;
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }

        .link-card h3 {
            font-size: 1.15em;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }

        .link-type {
            font-size: 0.75em;
            padding: 4px 8px;
            background: var(--sidebar-bg);
            border-radius: 4px;
            color: var(--text-secondary);
            white-space: nowrap;
        }

        .link-card .description {
            color: var(--text-secondary);
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 0;
        }

        /* 本地文件夹链接样式 */
        .card-actions.local-folder {
            background: rgba(34, 197, 94, 0.08) !important;
            border-right-color: rgba(34, 197, 94, 0.3) !important;
        }

        .card-actions a.local-path {
            background: transparent !important;
            color: #16a34a !important;
        }

        .card-actions a.local-path:hover {
            background: rgba(34, 197, 94, 0.15) !important;
            color: #15803d !important;
        }

        /* 本地路径图标特殊样式 */
        .card-actions a.local-path i {
            font-size: 1.1em;
        }

        /* 复制路径按钮 */
        .copy-path-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            padding: 0 16px;
            background: rgba(139, 92, 246, 0.08);
            color: var(--copy-btn-color);
            border: none;
            cursor: pointer;
            transition: var(--transition);
            font-size: 0.9em;
            border-left: 1px solid rgba(139, 92, 246, 0.2);
        }

        .copy-path-btn:hover {
            background: rgba(139, 92, 246, 0.4);
            color: var(--copy-btn-hover);
        }
        """

    @staticmethod
    def get_release_notes_styles():
        """发布说明样式"""
        return """
        /* 发布说明布局 */
        .release-types-sidebar {
            width: 250px;
            flex-shrink: 0;
        }

        .release-type-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 16px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: var(--transition);
            box-shadow: var(--shadow);
        }

        .release-type-card:hover {
            border-color: var(--primary-color);
            transform: translateY(-1px);
        }

        .release-type-card.active {
            border-color: var(--primary-color);
            background: rgba(99, 102, 241, 0.05);
        }

        .release-type-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }

        .release-type-icon {
            font-size: 1.5em;
        }

        .release-type-name {
            font-weight: 600;
            color: var(--text-primary);
            flex: 1;
        }

        .release-type-count {
            font-size: 0.8em;
            color: var(--text-secondary);
            background: var(--sidebar-bg);
            padding: 2px 6px;
            border-radius: 10px;
        }

        .release-type-description {
            color: var(--text-secondary);
            font-size: 0.85em;
            line-height: 1.4;
        }

        /* 时间轴布局 */
        .timeline-layout {
            display: flex;
            gap: 30px;
        }

        .timeline-container {
            flex: 1;
            position: relative;
        }

        .timeline {
            position: relative;
            padding: 20px 0;
        }

        .timeline::before {
            content: '';
            position: absolute;
            left: 30px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: var(--primary-color);
            opacity: 0.3;
        }

        .timeline-item {
            position: relative;
            margin-bottom: 30px;
            padding-left: 80px;
        }

        .timeline-date {
            position: absolute;
            left: 0;
            top: 0;
            width: 60px;
            padding: 8px 4px;
            background: var(--primary-color);
            color: white;
            border-radius: 6px;
            text-align: center;
            font-weight: 600;
            font-size: 0.85em;
        }

        /* 时间轴内容样式 */
        .timeline-content {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 20px;
            box-shadow: var(--shadow);
        }

        .timeline-content h3 {
            margin: 0 0 8px 0;
            color: var(--text-primary);
            font-size: 1.2em;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .timeline-content .version {
            display: inline-block;
            background: rgba(99, 102, 241, 0.1);
            color: var(--primary-color);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
            margin-right: 8px;
        }

        /* 主线版本样式 */
        .timeline-content .main-version {
            display: inline-block;
            background: rgba(34, 197, 94, 0.1);
            color: #16a34a;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: 500;
            margin-left: 8px;
            border: 1px solid rgba(34, 197, 94, 0.2);
        }

        /* 发布元信息样式 */
        .release-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 12px 0;
            padding: 12px;
            background: rgba(99, 102, 241, 0.03);
            border-radius: 6px;
            border-left: 3px solid var(--primary-color);
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85em;
            color: var(--text-secondary);
        }

        .meta-item i {
            font-size: 1em;
            opacity: 0.7;
        }

        .meta-label {
            font-weight: 600;
            color: var(--text-primary);
        }

        .meta-value {
            color: var(--text-secondary);
        }

        /* 开发人员样式 */
        .meta-item.dev {
            color: #7c3aed;
        }

        .meta-item.dev i {
            color: #7c3aed;
        }

        /* 分支信息样式 */
        .meta-item.branch {
            color: #0891b2;
        }

        .meta-item.branch i {
            color: #0891b2;
        }

        /* 标签样式 */
        .meta-item.tag {
            color: #dc2626;
        }

        .meta-item.tag i {
            color: #dc2626;
        }

        /* 提交信息样式 */
        .meta-item.commit {
            color: #ca8a04;
        }

        .meta-item.commit i {
            color: #ca8a04;
        }

        .timeline-content .description {
            color: var(--text-secondary);
            margin: 8px 0;
            line-height: 1.5;
        }

        .timeline-content .features {
            margin-top: 12px;
            padding-left: 20px;
        }

        .timeline-content .features li {
            margin: 4px 0;
            color: var(--text-secondary);
            font-size: 0.9em;
        }
        """

    @staticmethod
    def get_docs_styles():
        """配置说明和图标引用样式"""
        return """
        /* 配置说明和图标引用页面样式 */
        .docs-container {
            width: 100%;
            max-width: none;
        }

        .doc-section {
            margin-bottom: 30px;
            padding: 25px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            width: 100%;
            box-sizing: border-box;
        }

        .doc-section h3 {
            margin: 0 0 20px 0;
            color: var(--text-primary);
            font-size: 1.4em;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 10px;
        }

        .doc-section p {
            margin: 0 0 20px 0;
            color: var(--text-secondary);
            line-height: 1.6;
            font-size: 1em;
        }

        /* 配置表格样式 */
        .config-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9em;
            table-layout: fixed;
        }

        .config-table th {
            background: rgba(99, 102, 241, 0.1);
            color: var(--text-primary);
            font-weight: 600;
            padding: 14px 12px;
            text-align: left;
            border: 1px solid var(--border-color);
            word-wrap: break-word;
        }

        .config-table td {
            padding: 12px;
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            word-wrap: break-word;
        }

        .config-table code {
            background: rgba(99, 102, 241, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            color: var(--primary-color);
        }

        .config-table tr:nth-child(even) {
            background: rgba(99, 102, 241, 0.03);
        }

        .config-table tr:hover {
            background: rgba(99, 102, 241, 0.05);
        }

        /* 配置示例样式 */
        .config-example {
            margin: 20px 0;
            background: #1e1e1e;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            width: 100%;
        }

        .config-example pre {
            margin: 0;
            padding: 20px;
            overflow-x: auto;
        }

        .config-example code {
            color: #d4d4d4;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
        }

        /* 提示列表样式 */
        .tips-list {
            margin: 20px 0;
            padding-left: 22px;
            color: var(--text-secondary);
            width: 100%;
        }

        .tips-list li {
            margin: 10px 0;
            line-height: 1.6;
        }

        .tips-list strong {
            color: var(--text-primary);
        }

        /* 图标引用样式 */
        .icon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 15px;
            margin: 20px 0;
            width: 100%;
        }

        .svg-grid {
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        }

        .icon-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 16px 8px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            cursor: pointer;
            transition: var(--transition);
            text-align: center;
        }

        .icon-item:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
            border-color: var(--primary-color);
        }

        .icon-display {
            font-size: 2em;
            margin-bottom: 8px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .svg-display {
            width: 40px;
            height: 40px;
            color: oklch(55.2% 0.016 285.938);
        }

        .svg-display svg {
            width: 100%;
            height: 100%;
            /* 针对Lucide图标的特殊设置 */
            stroke: currentColor;
            fill: none;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        .icon-name {
            font-size: 0.8em;
            color: var(--text-primary);
            font-weight: 500;
            margin: 4px 0;
        }

        .icon-code {
            font-size: 0.7em;
            color: var(--text-secondary);
            font-family: monospace;
            background: var(--sidebar-bg);
            padding: 2px 6px;
            border-radius: 4px;
            margin: 4px 0;
        }

        .icon-id {
            font-size: 0.7em;
            color: oklch(55.2% 0.016 285.938);
            background: rgba(99, 102, 241, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            margin-top: 4px;
            font-family: monospace;
            font-weight: 500;
        }

        .icon-category {
            margin-bottom: 35px;
            width: 100%;
        }

        .icon-category:last-child {
            margin-bottom: 20px;
        }

        .icon-category h4 {
            margin: 0 0 15px 0;
            color: var(--text-primary);
            font-size: 1.2em;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
        }

        /* 图标提示区域 */
        .icon-tips {
            background: rgba(99, 102, 241, 0.05);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: var(--border-radius);
            padding: 20px;
            margin: 20px 0;
            width: 100%;
            box-sizing: border-box;
        }

        .icon-tips h4 {
            margin: 0 0 15px 0;
            color: var(--text-primary);
            font-size: 1.1em;
        }

        /* 导航项中的SVG图标 */
        .nav-item i .svg-icon {
            width: 20px;
            height: 20px;
        }

        .nav-item i .svg-icon svg {
            width: 100%;
            height: 100%;
            stroke: currentColor;
            fill: none;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        /* 发布类型卡片中的SVG图标 */
        .release-type-icon .svg-icon {
            width: 24px;
            height: 24px;
        }

        .release-type-icon .svg-icon svg {
            width: 100%;
            height: 100%;
            stroke: currentColor;
            fill: none;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }
        """

    @staticmethod
    def get_ui_styles():
        """UI组件样式"""
        return """
        /* 简洁版使用说明 */
        .usage-help {
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 40px;
            height: 40px;
            background: var(--primary-color);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: var(--shadow-hover);
            z-index: 999;
            font-size: 1.2em;
            transition: var(--transition);
        }

        .usage-help:hover {
            transform: scale(1.1);
            background: var(--primary-hover);
        }

        .usage-tooltip {
            position: fixed;
            bottom: 130px;
            right: 20px;
            width: 400px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 20px;
            box-shadow: var(--shadow-hover);
            z-index: 1000;
            display: none;
        }

        .usage-tooltip.show {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        .usage-tooltip h3 {
            margin: 0 0 12px 0;
            font-size: 1.1em;
            color: var(--text-primary);
        }

        .usage-tooltip ul {
            margin: 0;
            padding-left: 18px;
            color: var(--text-secondary);
        }

        .usage-tooltip li {
            margin: 6px 0;
            font-size: 0.9em;
            line-height: 1.4;
        }

        /* 页脚样式 */
        .footer {
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid var(--border-color);
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.9em;
        }

        .footer p {
            margin: 4px 0;
        }

        /* 开发者信息和徽章样式 */
        .developer-info {
            margin: 8px 0;
            color: var(--text-secondary);
            font-size: 0.85em;
            opacity: 0.8;
        }

        .generator-info {
            opacity: 0.7;
            font-size: 0.85em;
        }

        /* 统计信息 - 固定在右下角 */
        .stats {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 0.85em;
            color: var(--text-secondary);
            box-shadow: var(--shadow);
            backdrop-filter: blur(10px);
            z-index: 1000;
        }

        /* 通知消息样式 */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateX(150%);
            transition: transform 0.3s ease;
        }

        .notification.show {
            transform: translateX(0);
        }

        .notification.success {
            background: var(--success-color);
        }

        .notification.error {
            background: var(--error-color);
        }

        .notification.warning {
            background: var(--warning-color);
        }

        /* 模态框样式 */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 10000;
        }

        .modal-overlay.show {
            display: flex;
        }

        .modal {
            background: white;
            border-radius: 12px;
            padding: 24px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }

        .modal h3 {
            margin-bottom: 16px;
            color: var(--text-primary);
        }

        .modal p {
            margin-bottom: 20px;
            color: var(--text-secondary);
        }

        .modal-actions {
            display: flex;
            gap: 12px;
            justify-content: flex-end;
        }

        .modal-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            transition: var(--transition);
        }

        .modal-btn.primary {
            background: var(--primary-color);
            color: white;
        }

        .modal-btn.secondary {
            background: var(--sidebar-bg);
            color: var(--text-secondary);
        }

        .modal-btn:hover {
            opacity: 0.9;
        }
        """

    @staticmethod
    def get_version_tag_styles():
        """版本标签样式"""
        return """
        /* 简洁优雅的版本标签 */
        .version-tag {
            display: inline-flex;
            align-items: center;
            height: 24px;
            border-radius: 12px;
            padding: 0 12px;
            background: linear-gradient(135deg, #2ea043, #2c974b);
            color: white;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 12px;
            font-weight: 600;
            line-height: 1;
            margin-left: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            white-space: nowrap;
        }

        .version-tag::before {
            content: "🗂️";
            margin-right: 4px;
            font-size: 11px;
            opacity: 0.9;
        }

        /* 可选：不同的版本类型 */
        .version-tag.beta {
            background: linear-gradient(135deg, #fbca04, #e0b003);
            color: #333;
        }

        .version-tag.alpha {
            background: linear-gradient(135deg, #e05d44, #c94a32);
        }

        .version-tag.stable {
            background: linear-gradient(135deg, #2ea043, #2c974b);
        }

        .version-tag.release {
            background: linear-gradient(135deg, #007ec6, #0069a7);
        }

        /* 悬停效果 */
        .version-tag:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }

        /* 在时间轴中的样式 */
        .timeline-content .version-tag {
            margin-left: 8px;
            vertical-align: middle;
        }
        """

    @staticmethod
    def get_responsive_styles():
        """响应式设计"""
        return """
        /* 响应式设计 */
        @media (max-width: 1024px) {
            .main-content {
                padding: 30px 40px;
            }
            .cards-container.grid-layout {
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            }
        }

        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
                border-right: none;
                border-bottom: 1px solid var(--border-color);
            }
            .main-content {
                margin-left: 0;
                padding: 20px 25px;
                max-width: 100%;
            }
            body {
                flex-direction: column;
            }
            .section-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }
            .layout-controls {
                align-self: flex-end;
            }
            .link-card {
                flex-direction: column;
            }
            .card-actions {
                border-right: none;
                border-bottom: 1px solid var(--border-color);
                width: 100%;
            }
            .link-card a {
                padding: 16px 24px;
                justify-content: flex-start;
            }
            .card-content {
                padding: 16px 20px;
            }
            .cards-container.grid-layout {
                grid-template-columns: 1fr;
            }

            /* 移动端标签样式调整 */
            .tag-container {
                writing-mode: horizontal-tb;
                padding: 4px 8px;
                min-width: auto;
                border-right: none;
                border-bottom: 1px solid rgba(139, 92, 246, 0.2);
            }
            .link-tag {
                transform: none;
            }

            /* 移动端时间轴调整 */
            .timeline-layout {
                flex-direction: column;
            }
            .release-types-sidebar {
                width: 100%;
                order: 2;
            }
            .timeline-container {
                order: 1;
            }
            .timeline::before {
                left: 15px;
            }
            .timeline-item {
                padding-left: 50px;
            }
            .timeline-date {
                width: 40px;
                font-size: 0.75em;
            }

            /* 移动端元信息调整 */
            .release-meta {
                flex-direction: column;
                gap: 8px;
            }

            .meta-item {
                justify-content: space-between;
            }

            .timeline-content .main-version {
                display: block;
                margin: 4px 0 0 0;
                width: fit-content;
            }

            /* 移动端统计信息 */
            .stats {
                bottom: 10px;
                right: 10px;
                font-size: 0.8em;
                padding: 10px 12px;
            }

            /* 移动端文档样式 */
            .doc-section {
                padding: 18px;
                margin-bottom: 20px;
            }

            .doc-section h3 {
                font-size: 1.2em;
                margin-bottom: 15px;
            }

            .icon-grid {
                grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
                gap: 12px;
            }

            .svg-grid {
                grid-template-columns: repeat(auto-fill, minmax(85px, 1fr));
            }

            .config-table {
                font-size: 0.8em;
                display: block;
                overflow-x: auto;
            }

            .config-table th,
            .config-table td {
                padding: 10px 8px;
                min-width: 80px;
            }

            .config-example pre {
                padding: 15px;
            }

            .config-example code {
                font-size: 0.8em;
            }

            /* 移动端接口路由样式 */
            .interface-route-container {
                padding: 15px;
            }

            .control-group {
                flex-direction: column;
                align-items: flex-start;
            }

            .interface-table-container {
                font-size: 0.8em;
            }

            .interface-table th,
            .interface-table td {
                padding: 8px 6px;
            }
        }

        @media (max-width: 480px) {
            .main-content {
                padding: 16px 18px;
            }
            .link-card {
                padding: 0;
            }
            .card-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }
            .layout-controls {
                align-self: stretch;
                justify-content: space-between;
            }
            .layout-btn {
                flex: 1;
                text-align: center;
            }

            /* 小屏幕文档样式 */
            .doc-section {
                padding: 15px;
            }

            .icon-grid {
                grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
                gap: 10px;
            }

            .svg-grid {
                grid-template-columns: repeat(auto-fill, minmax(75px, 1fr));
            }

            .config-table {
                font-size: 0.75em;
            }

            .config-table th,
            .config-table td {
                padding: 8px 6px;
            }

            .icon-tips {
                padding: 15px;
            }

            /* 小屏幕接口路由样式 */
            .route-title {
                font-size: 1.3em;
            }

            .view-filter, .branch-filter {
                padding: 6px 12px;
                font-size: 0.8em;
            }
        }
        """

    @staticmethod
    def get_interface_route_styles():
        """接口路由专用样式"""
        return """
        /* 版本接口样式 */
        .interface-route-container {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
        }

        .route-title {
            font-size: 1.5em;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .route-description {
            color: var(--text-secondary);
            margin-bottom: 20px;
            font-size: 0.95em;
        }

        /* 控制面板样式 */
        .control-panel {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
        }

        .control-group {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: center;
            margin-bottom: 15px;
        }

        .control-label {
            font-weight: 600;
            color: var(--text-primary);
            min-width: 80px;
        }

        .view-filters {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .view-filter {
            padding: 8px 16px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            cursor: pointer;
            transition: var(--transition);
            font-size: 0.9em;
            color: var(--text-secondary);
        }

        .view-filter:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
        }

        .view-filter.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }

        .branch-filters {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .branch-filter {
            padding: 6px 12px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            cursor: pointer;
            transition: var(--transition);
            font-size: 0.85em;
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-secondary);
        }

        .branch-filter:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
        }

        .branch-filter.active {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }

        .branch-color-indicator {
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }

        /* 接口表格样式 */
        .interface-table-container {
            overflow-x: auto;
            margin-top: 15px;
        }

        .interface-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }

        .interface-table th,
        .interface-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        .interface-table th {
            background: var(--sidebar-bg);
            font-weight: 600;
            color: var(--text-primary);
            position: sticky;
            top: 0;
        }

        .interface-table tr:hover {
            background: rgba(99, 102, 241, 0.05);
        }

        .interface-table td {
            color: var(--text-secondary);
        }

        /* 分支列样式 */
        .branch-cell {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .branch-color {
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }

        .branch-name {
            font-weight: 500;
        }

        /* 标签样式 */
        .tag {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 500;
            white-space: nowrap;
        }

        .tag.released {
            background: rgba(16, 185, 129, 0.1);
            color: #065f46;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .tag.deprecated {
            background: rgba(245, 158, 11, 0.1);
            color: #92400e;
            border: 1px solid rgba(245, 158, 11, 0.2);
        }

        .tag.removed {
            background: rgba(239, 68, 68, 0.1);
            color: #991b1b;
            border: 1px solid rgba(239, 68, 68, 0.2);
        }

        .tag.development {
            background: rgba(99, 102, 241, 0.1);
            color: #3730a3;
            border: 1px solid rgba(99, 102, 241, 0.2);
        }

        .tag.planning {
            background: rgba(107, 114, 128, 0.1);
            color: #374151;
            border: 1px solid rgba(107, 114, 128, 0.2);
        }

        /* 版本号样式 */
        .version-id {
            font-weight: 600;
            color: var(--text-primary);
        }

        /* 分支分组样式 */
        .branch-group {
            margin-bottom: 30px;
        }

        .branch-header {
            padding: 12px 16px;
            border-radius: 8px 8px 0 0;
            margin-bottom: 0;
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--primary-color);
            color: white;
        }

        .branch-header div:first-child {
            font-weight: 600;
            font-size: 1.1em;
        }

        .branch-header div:last-child {
            font-size: 0.9em;
            opacity: 0.9;
        }

        .view-content {
            transition: var(--transition);
        }
        """

    @staticmethod
    def get_all_styles():
        """获取所有CSS样式"""
        styles = [
            CSSManager.get_base_styles(),
            CSSManager.get_layout_styles(),
            CSSManager.get_logo_styles(),
            CSSManager.get_section_styles(),
            CSSManager.get_card_styles(),
            CSSManager.get_release_notes_styles(),
            CSSManager.get_docs_styles(),
            CSSManager.get_ui_styles(),
            CSSManager.get_version_tag_styles(),
            CSSManager.get_interface_route_styles(),
            CSSManager.get_responsive_styles()
        ]
        return "\n".join(styles)

class InterfaceRouteGenerator:
    def __init__(self, title="版本接口"):
        self.title = title
        self.interface_routes = {}  # 存储版本仓库数据
        self.generator_info = "InterfaceRouteTable v2.0 | 分支分组表格 | 标签状态 | 开发者: @wanqiang.liu"

    def add_interface_route(self, route_name, route_data):
        """添加版本仓库"""
        self.interface_routes[route_name] = route_data

    def _generate_interface_route_html(self, route_name, route_data):
        """生成版本仓库HTML"""
        
        # 收集所有接口名称
        all_interfaces = set()
        for version_id, version_data in route_data['versions'].items():
            interfaces = self._parse_interfaces(version_data.get('interfaces', ''))
            all_interfaces.update([iface for iface, ver in interfaces])
        
        # 生成视图切换器
        view_filters_html = """
            <button class="view-filter active" data-view="unified">统一视图</button>
            <button class="view-filter" data-view="grouped">分组视图</button>
        """
        
        # 生成分支筛选器
        branch_filters_html = '<button class="branch-filter active" data-branch="all">全部</button>'
        for branch_id, branch_data in route_data['branches'].items():
            name = branch_data.get('name', branch_id)
            color = branch_data.get('color', '#6366f1')
            branch_filters_html += f'''
            <button class="branch-filter" data-branch="{branch_id}">
                <div class="branch-color-indicator" style="background: {color};"></div>
                {name}
            </button>'''
        
        # 生成统一视图表格
        unified_table_html = self._generate_unified_table(route_data, sorted(all_interfaces))
        
        # 生成分组视图表格
        grouped_tables_html = self._generate_grouped_tables(route_data, sorted(all_interfaces))
        
        html = f"""
        <div class="interface-route-container">
            <div class="route-title">
                <span>{route_name}</span>
            </div>
            <div class="route-description">
                {route_data.get('description', '接口版本演变路线')}
            </div>
            
            <div class="control-panel">
                <div class="control-group">
                    <div class="control-label">视图模式:</div>
                    <div class="view-filters">
                        {view_filters_html}
                    </div>
                </div>
                <div class="control-group">
                    <div class="control-label">分支筛选:</div>
                    <div class="branch-filters">
                        {branch_filters_html}
                    </div>
                </div>
            </div>
            
            <!-- 统一视图 -->
            <div class="view-content" data-view="unified">
                {unified_table_html}
            </div>
            
            <!-- 分组视图 -->
            <div class="view-content" data-view="grouped" style="display: none;">
                {grouped_tables_html}
            </div>
        </div>
        """
        
        return html

    def _generate_unified_table(self, route_data, all_interfaces):
        """生成统一视图表格"""
        # 按日期排序版本
        sorted_versions = sorted(
            route_data['versions'].items(),
            key=lambda x: x[1].get('date', '')
        )
        
        table_html = """
        <div class="interface-table-container">
            <table class="interface-table">
                <thead>
                    <tr>
                        <th>版本</th>
                        <th>分支</th>
                        <th>日期</th>
                        <th>标签</th>
                        <th>父版本</th>
                        <th>合并目标</th>
                        <th>描述</th>
        """
        
        # 添加接口列
        for interface in all_interfaces:
            table_html += f'<th>{interface}</th>'
        
        table_html += """
                    </tr>
                </thead>
                <tbody>
        """
        
        # 添加版本行
        for version_id, version_data in sorted_versions:
            branch_id = version_data.get('branch', 'master')
            branch_data = route_data['branches'].get(branch_id, {})
            branch_name = branch_data.get('name', branch_id)
            branch_color = branch_data.get('color', '#6366f1')
            
            interfaces_dict = dict(self._parse_interfaces(version_data.get('interfaces', '')))
            tag = version_data.get('tag', '')
            tag_class = self._get_tag_class(tag)
            
            table_html += f"""
                    <tr data-branch="{branch_id}">
                        <td><span class="version-id">{version_id}</span></td>
                        <td>
                            <div class="branch-cell">
                                <div class="branch-color" style="background: {branch_color};"></div>
                                <span class="branch-name">{branch_name}</span>
                            </div>
                        </td>
                        <td>{version_data.get('date', '')}</td>
                        <td>{f'<span class="tag {tag_class}">{tag}</span>' if tag else '-'}</td>
                        <td>{version_data.get('parent', '-')}</td>
                        <td>{version_data.get('merge_target', '-')}</td>
                        <td>{version_data.get('description', '')}</td>
            """
            
            for interface in all_interfaces:
                version = interfaces_dict.get(interface, '-')
                table_html += f'<td>{version}</td>'
            
            table_html += '</tr>'
        
        table_html += """
                </tbody>
            </table>
        </div>
        """
        
        return table_html

    def _generate_grouped_tables(self, route_data, all_interfaces):
        """生成分组视图表格"""
        # 按分支分组版本
        branch_versions = defaultdict(list)
        for version_id, version_data in route_data['versions'].items():
            branch = version_data.get('branch', 'master')
            branch_versions[branch].append((version_id, version_data))
        
        # 对每个分支的版本按日期排序
        for branch, versions in branch_versions.items():
            versions.sort(key=lambda x: x[1].get('date', ''))
        
        branch_tables_html = ""
        for branch_id, branch_data in sorted(route_data['branches'].items()):
            versions = branch_versions.get(branch_id, [])
            if not versions:
                continue
                
            branch_name = branch_data.get('name', branch_id)
            branch_description = branch_data.get('description', '')
            branch_color = branch_data.get('color', '#6366f1')
            
            branch_tables_html += f"""
            <div class="branch-group" data-branch="{branch_id}">
                <div class="branch-header" style="background: {branch_color}; color: white;">
                    <div>{branch_name}</div>
                    <div>{branch_description}</div>
                </div>
                <div class="interface-table-container">
                    <table class="interface-table">
                        <thead>
                            <tr>
                                <th>版本</th>
                                <th>日期</th>
                                <th>标签</th>
                                <th>父版本</th>
                                <th>合并目标</th>
                                <th>描述</th>
            """
            
            # 添加接口列
            for interface in all_interfaces:
                branch_tables_html += f'<th>{interface}</th>'
            
            branch_tables_html += """
                            </tr>
                        </thead>
                        <tbody>
            """
            
            # 添加版本行
            for version_id, version_data in versions:
                interfaces_dict = dict(self._parse_interfaces(version_data.get('interfaces', '')))
                tag = version_data.get('tag', '')
                tag_class = self._get_tag_class(tag)
                
                branch_tables_html += f"""
                            <tr>
                                <td><span class="version-id">{version_id}</span></td>
                                <td>{version_data.get('date', '')}</td>
                                <td>{f'<span class="tag {tag_class}">{tag}</span>' if tag else '-'}</td>
                                <td>{version_data.get('parent', '-')}</td>
                                <td>{version_data.get('merge_target', '-')}</td>
                                <td>{version_data.get('description', '')}</td>
                """
                
                for interface in all_interfaces:
                    version = interfaces_dict.get(interface, '-')
                    branch_tables_html += f'<td>{version}</td>'
                
                branch_tables_html += '</tr>'
            
            branch_tables_html += """
                        </tbody>
                    </table>
                </div>
            </div>
            """
        
        return branch_tables_html

    def _parse_interfaces(self, interfaces_input):
        """解析接口输入，支持多种格式"""
        interfaces = []

        if not interfaces_input:
            return interfaces

        # 处理字符串格式
        if isinstance(interfaces_input, str):
            for item in interfaces_input.split(','):
                item = item.strip()
                if ':' in item:
                    iface, ver = item.split(':', 1)
                    interfaces.append((iface.strip(), ver.strip()))
                elif item:  # 非空字符串
                    interfaces.append((item.strip(), 'v1.0'))

        # 处理列表格式
        elif isinstance(interfaces_input, list):
            for item in interfaces_input:
                if isinstance(item, str):
                    if ':' in item:
                        iface, ver = item.split(':', 1)
                        interfaces.append((iface.strip(), ver.strip()))
                    else:
                        interfaces.append((item.strip(), 'v1.0'))
                elif isinstance(item, dict) and 'name' in item and 'version' in item:
                    interfaces.append((str(item['name']).strip(), str(item['version']).strip()))
                elif isinstance(item, dict) and 'name' in item:
                    interfaces.append((str(item['name']).strip(), 'v1.0'))

        return interfaces

    def _get_tag_class(self, tag):
        """根据标签内容获取CSS类名"""
        tag_lower = tag.lower()
        if '启用' in tag_lower or '发版' in tag_lower or '发布' in tag_lower:
            return 'released'
        elif '弃用' in tag_lower or '废弃' in tag_lower:
            return 'deprecated'
        elif '移除' in tag_lower or '删除' in tag_lower:
            return 'removed'
        elif '开发' in tag_lower or '测试' in tag_lower:
            return 'development'
        elif '规划' in tag_lower or '计划' in tag_lower:
            return 'planning'
        else:
            return 'released'  # 默认

    def generate_interface_routes_html(self):
        """生成版本接口HTML内容"""
        if not self.interface_routes:
            return ""
        
        content_sections = ""
        for route_name, route_data in self.interface_routes.items():
            content_sections += self._generate_interface_route_html(route_name, route_data)
        
        return content_sections


class SoftNavGenerator:
    def __init__(self, title="嵌入式开发中心", default_layout="list"):
        self.title = title
        self.default_layout = default_layout  # "list" 或 "grid"
        self.categories = {}
        self.release_notes = {}  # 专门存储发布说明数据
        self.interface_routes = InterfaceRouteGenerator()  # 版本仓库生成器
        self.generator_info = "SoftNavGenerator v3.7 | 增强本地文件夹支持 | 时间轴功能 | 版本接口 | 开发者: @wanqiang.liu"
        self.css_style = CSSManager.get_all_styles()
        self.js_script = JavaScriptManager.get_all_scripts()

    def add_category(self, category_name, links_list, icon="📁", category_type="工具"):
        """添加分类和链接

        Args:
            category_name: 分类名称
            links_list: 链接列表，格式 [["链接名", "URL", "描述", "类型", "标签"], ...]
            icon: 分类图标
            category_type: 分类类型
        """
        self.categories[category_name] = {
            "icon": icon,
            "type": category_type,
            "links": links_list
        }

    def add_release_note(self, release_type, releases):
        """添加发布说明

        Args:
            release_type: 发布类型（如：功能降级、故障管理等）
            releases: 发布列表，每个发布包含版本、日期、描述等
        """
        # 确保每个release的details字段是字符串格式（分号分隔）
        processed_releases = []
        for release in releases:
            processed_release = release.copy()

            # 处理details字段：如果是列表，转换为分号分隔的字符串
            details = release.get('details', '')
            if isinstance(details, list):
                processed_release['details'] = ';'.join(str(item) for item in details)
            elif isinstance(details, str):
                processed_release['details'] = details
            else:
                processed_release['details'] = ''

            processed_releases.append(processed_release)

        self.release_notes[release_type] = processed_releases

    def _generate_normal_category_section(self, category_name, category_data, active_class):
        """生成普通分类页面"""
        # 修复问题1：正确使用配置的默认布局
        default_layout_class = "list-layout" if self.default_layout == "list" else "grid-layout"
        default_list_btn_active = "active" if self.default_layout == "list" else ""
        default_grid_btn_active = "active" if self.default_layout == "grid" else ""

        # 收集所有标签用于筛选
        all_tags = set()
        for link_data in category_data["links"]:
            if len(link_data) >= 5:
                tag = link_data[4]
                if tag:
                    all_tags.add(tag)

        # 生成标签筛选器
        tag_filters_html = ""
        if all_tags:
            tag_filters_html = '<div class="tag-filters">'
            tag_filters_html += '<div class="tag-filter active" data-tag="全部">全部</div>'
            for tag in sorted(all_tags):
                tag_filters_html += f'<div class="tag-filter" data-tag="{tag}">{tag}</div>'
            tag_filters_html += '</div>'

        # 关键修复：确保使用正确的默认布局类
        category_section = f"""
            <div class="category-section {active_class}" id="{category_name}">
                <div class="section-header">
                    <div class="section-title">
                        <h2>{category_name}</h2>
                        <p>发现 {len(category_data['links'])} 个精选资源</p>
                    </div>
                    <div class="layout-controls">
                        <button class="layout-btn {default_list_btn_active}" data-layout="list">列表视图</button>
                        <button class="layout-btn {default_grid_btn_active}" data-layout="grid">格子视图</button>
                    </div>
                </div>
                {tag_filters_html}
                <div class="cards-container {default_layout_class}">
        """

        for link_data in category_data["links"]:
            if len(link_data) == 3:
                link_name, url, description = link_data
                link_type = "网站"
                tag = ""
            elif len(link_data) == 4:
                link_name, url, description, link_type = link_data
                tag = link_type if link_type != "网站" else ""
            else:
                link_name, url, description, link_type, tag = link_data

            # 检测是否为本地路径
            is_local_path = False
            local_path_icon = "🔗"
            local_path_text = "访问"

            original_path = url
            if (url.startswith(r'\\') or '本地文件夹' in link_type):
                is_local_path = True
                local_path_icon = "📁"
                local_path_text = "打开"

            # 为本地文件夹添加复制路径按钮
            copy_button = ""
            if is_local_path:
                copy_button = f"""
                    <button class="copy-path-btn" data-path="{original_path}" title="复制路径">
                        <i>Copy</i>
                    </button>
                """

            # 添加标签容器
            tag_html = ""
            if tag:
                tag_html = f"""
                    <div class="tag-container">
                        <span class="link-tag">{tag}</span>
                    </div>
                """

            # 添加数据标签属性用于筛选
            data_tag_attr = f'data-tags="{tag}"' if tag else ""

            category_section += f"""
                    <div class="link-card" data-is-local="{str(is_local_path).lower()}" data-original-path="{original_path}" {data_tag_attr}>
                        <div class="card-actions {'local-folder' if is_local_path else ''}">
                            <a href="{url}" target="_blank" title="{local_path_text} {link_name}" class="{'local-path' if is_local_path else ''}">
                                <i>{local_path_icon}</i>
                                {local_path_text}
                            </a>
                            {tag_html}
                            {copy_button}
                        </div>
                        <div class="card-content">
                            <div class="card-info">
                                <div class="card-header">
                                    <h3>{link_name}</h3>
                                    <span class="link-type">{link_type}</span>
                                </div>
                                <p class="description">{description}</p>
                            </div>
                        </div>
                    </div>
            """

        category_section += """
                </div>
            </div>
        """
        return category_section

    def _generate_release_notes_section(self, category_name, active_class):
        """生成发布说明页面"""
        category_section = f"""
            <div class="category-section {active_class}" id="{category_name}">
                <div class="section-header">
                    <div class="section-title">
                        <h2>{category_name}</h2>
                        <p>版本历史与更新日志</p>
                    </div>
                </div>
        """

        if self.release_notes:
            category_section += """
                <div class="timeline-layout">
                    <!-- 左侧发布类型列表 -->
                    <div class="release-types-sidebar">
            """

            # 生成发布类型卡片
            for j, (release_type, releases) in enumerate(self.release_notes.items()):
                active_card_class = "active" if j == 0 else ""
                icon = releases[0].get('icon', '📋') if releases else '📋'
                count = len(releases)
                description = releases[0].get('type_description', '') if releases else ''

                category_section += f"""
                        <div class="release-type-card {active_card_class}" data-release-type="{release_type}">
                            <div class="release-type-header">
                                <div class="release-type-icon">{icon}</div>
                                <div class="release-type-name">{release_type}</div>
                                <div class="release-type-count">{count}</div>
                            </div>
                            <div class="release-type-description">{description}</div>
                        </div>
                """

            category_section += """
                    </div>
                    <!-- 右侧时间轴容器 -->
                    <div class="timeline-container">
            """

            # 为每个发布类型生成时间轴
            for j, (release_type, releases) in enumerate(self.release_notes.items()):
                display_style = "block" if j == 0 else "none"
                category_section += f"""
                        <div class="timeline" id="timeline-{release_type}" style="display: {display_style};">"""

                for release in reversed(releases):
                    version = release.get('version', '')
                    date = release.get('date', '')
                    description = release.get('description', '')
                    details = release.get('details', '')

                    # 新增字段
                    main_version = release.get('main_version', '')
                    dev = release.get('dev', '')
                    branch = release.get('branch', '')
                    tag = release.get('tag', '')
                    commit = release.get('commit', '')

                    # 解析特性列表
                    features_html = ""
                    if details:
                        if isinstance(details, str):
                            features = [f.strip() for f in details.split(';') if f.strip()]
                        else:
                            features = details
                        if features:
                            features_html = "<ul class='features'>" + "".join(
                                [f"<li>{f}</li>" for f in features]) + "</ul>"

                    # 生成元信息HTML
                    meta_html = ""
                    if main_version or dev or branch or tag or commit:
                        meta_html = '<div class="release-meta">'

                        if main_version:
                            meta_html += f'<div class="meta-item"><i>📦</i><span class="meta-label">主线版本:</span><span class="meta-value">{main_version}</span></div>'

                        if dev:
                            meta_html += f'<div class="meta-item dev"><i>👤</i><span class="meta-label">开发:</span><span class="meta-value">{dev}</span></div>'

                        if branch:
                            meta_html += f'<div class="meta-item branch"><i>🌿</i><span class="meta-label">分支:</span><span class="meta-value">{branch}</span></div>'

                        if tag:
                            meta_html += f'<div class="meta-item tag"><i>🏷️</i><span class="meta-label">标签:</span><span class="meta-value">{tag}</span></div>'

                        if commit:
                            # 如果提交哈希较长，可以截取前7位
                            commit_display = commit[:7] if len(commit) > 7 else commit
                            meta_html += f'<div class="meta-item commit"><i>🔗</i><span class="meta-label">提交:</span><span class="meta-value">{commit_display}</span></div>'

                        meta_html += '</div>'

                    # 版本标签
                    version_html = f'<span class="version-tag stable">{release_type}:{str(version).upper()}</span>' if version else ''
                    main_version_html = f'<span class="version-tag beta">软件版本:{str(main_version).upper()}</span>' if main_version else ''

                    category_section += f"""
                            <div class="timeline-item">
                                <div class="timeline-date">{date}</div>
                                <div class="timeline-content">
                                    <h3>{version_html} {main_version_html}</h3>
                                    {meta_html}
                                    <p class="description">{description}</p>
                                    {features_html}
                                </div>
                            </div>
                    """

                category_section += """
                        </div>
                """

            category_section += """
                    </div>
                </div>
            """
        else:
            category_section += """
                <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
                    <p>暂无发布说明数据</p>
                </div>
            """

        category_section += """
            </div>
        """
        return category_section

    def _generate_interface_map_section(self, category_name, active_class):
        """生成版本接口页面"""
        if self.interface_routes.interface_routes:
            interface_routes_content = self.interface_routes.generate_interface_routes_html()
        else:
            interface_routes_content = """
                <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
                    <p>暂无版本接口数据</p>
                </div>
            """

        return f"""
            <div class="category-section {active_class}" id="{category_name}">
                <div class="section-header">
                    <div class="section-title">
                        <h2>{category_name}</h2>
                        <p>Git分支演变与接口版本管理</p>
                    </div>
                </div>
                {interface_routes_content}
            </div>
        """

    def _generate_config_docs_section(self, category_name, active_class):
        """生成配置说明页面"""
        config_docs_content = self._generate_config_documentation()

        return f"""
            <div class="category-section {active_class}" id="{category_name}">
                <div class="section-header">
                    <div class="section-title">
                        <h2>{category_name}</h2>
                        <p>JSON配置文件语法和选项说明</p>
                    </div>
                </div>
                <div class="config-docs">
                    {config_docs_content}
                </div>
            </div>
        """

    def _generate_icons_reference_section(self, category_name, active_class):
        """生成图标引用页面"""
        icons_reference_content = self._generate_icons_reference()

        return f"""
            <div class="category-section {active_class}" id="{category_name}">
                <div class="section-header">
                    <div class="section-title">
                        <h2>{category_name}</h2>
                        <p>Emoji和SVG图标库，支持点击复制</p>
                    </div>
                </div>
                <div class="config-docs">
                    {icons_reference_content}
                </div>
            </div>
        """

    def _generate_config_documentation(self):
        """生成配置文档内容"""
        return """
        <div class="docs-container">
            <div class="doc-section">
                <h3>📋 配置文件结构 (JSON格式)</h3>
                <p>导航网站使用JSON格式配置文件，结构清晰，易于编辑和维护。采用类型化的设计模式，每种页面类型有独立的数据区域。</p>

                <div class="config-example">
                    <pre><code>{
        "site": {
            "title": "网站标题",
            "default_layout": "list"  // "list" 或 "grid"
        },
        "categories": [
            {
                "name": "分类名称",
                "icon": "📁",
                "type": "页面类型"  // 普通分类、ReleaseNotes、InterfaceMap等
            }
        ],
        "普通分类": {
            "分类名称1": {
                "links": [
                    {
                        "name": "链接名称",
                        "url": "https://example.com",
                        "description": "链接描述",
                        "type": "网站类型",
                        "tag": "标签名称"
                    }
                ]
            }
        },
        "ReleaseNotes": {
            "发布类型1": {
                "icon": "📋",
                "type_description": "类型描述",
                "releases": [
                    {
                        "version": "v1.0.0",
                        "date": "2024-01-01",
                        "main_version": "v2.0.0",
                        "dev": "开发人员",
                        "branch": "分支名称",
                        "tag": "标签名称",
                        "commit": "提交哈希",
                        "description": "版本描述",
                        "details": ["功能详情1", "功能详情2", "功能详情3"]
                    }
                ]
            }
        },
        "InterfaceMap": {
            "版本仓库名称": {
                "description": "版本仓库描述",
                "branches": {
                    "分支ID": {
                        "name": "分支显示名称",
                        "description": "分支描述",
                        "color": "#6366f1"
                    }
                },
                "versions": {
                    "版本ID": {
                        "branch": "分支ID",
                        "date": "2024-01-01",
                        "description": "版本描述",
                        "interfaces": ["接口1:v1.0", "接口2:v1.1"],
                        "parent": "父版本ID",
                        "merge_target": "合并目标版本",
                        "tag": "版本标签"
                    }
                }
            }
        }
    }</code></pre>
                </div>
            </div>

            <div class="doc-section">
                <h3>🏗️ 站点配置 (site)</h3>
                <table class="config-table">
                    <thead>
                        <tr>
                            <th>字段名</th>
                            <th>类型</th>
                            <th>必选</th>
                            <th>默认值</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>title</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>嵌入式开发中心</td>
                            <td>网站标题，显示在浏览器标签和页面顶部</td>
                        </tr>
                        <tr>
                            <td><code>default_layout</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>list</td>
                            <td>默认布局方式，支持 <code>"list"</code>（列表）或 <code>"grid"</code>（格子）</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="doc-section">
                <h3>📁 分类导航配置 (categories)</h3>
                <p>定义左侧导航栏的页面列表，每个分类对应一个页面。</p>

                <table class="config-table">
                    <thead>
                        <tr>
                            <th>字段名</th>
                            <th>类型</th>
                            <th>必选</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>name</code></td>
                            <td>string</td>
                            <td>是</td>
                            <td>页面名称，显示在导航栏</td>
                        </tr>
                        <tr>
                            <td><code>icon</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>页面图标，支持emoji</td>
                        </tr>
                        <tr>
                            <td><code>type</code></td>
                            <td>string</td>
                            <td>是</td>
                            <td>页面类型，决定页面的内容和行为</td>
                        </tr>
                    </tbody>
                </table>

                <h4>📋 页面类型说明</h4>
                <table class="config-table">
                    <thead>
                        <tr>
                            <th>类型值</th>
                            <th>说明</th>
                            <th>对应数据区域</th>
                            <th>示例</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>普通分类</code></td>
                            <td>普通链接分类页面</td>
                            <td><code>普通分类</code></td>
                            <td><code>{"name": "开发工具", "icon": "🛠️", "type": "普通分类"}</code></td>
                        </tr>
                        <tr>
                            <td><code>ReleaseNotes</code></td>
                            <td>发布说明页面，显示时间轴</td>
                            <td><code>ReleaseNotes</code></td>
                            <td><code>{"name": "发布说明", "icon": "📋", "type": "ReleaseNotes"}</code></td>
                        </tr>
                        <tr>
                            <td><code>InterfaceMap</code></td>
                            <td>版本接口页面，显示Git分支演变</td>
                            <td><code>InterfaceMap</code></td>
                            <td><code>{"name": "版本接口", "icon": "📊", "type": "InterfaceMap"}</code></td>
                        </tr>
                        <tr>
                            <td><code>ConfigDocs</code></td>
                            <td>配置说明页面（自动生成）</td>
                            <td>无需配置</td>
                            <td><code>{"name": "配置说明", "icon": "📖", "type": "ConfigDocs"}</code></td>
                        </tr>
                        <tr>
                            <td><code>IconsReference</code></td>
                            <td>图标引用页面（自动生成）</td>
                            <td>无需配置</td>
                            <td><code>{"name": "图标引用", "icon": "🎨", "type": "IconsReference"}</code></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="doc-section">
                <h3>🔗 普通分类配置 (普通分类)</h3>
                <p>定义普通分类页面的链接内容。键名为分类名称，与<code>categories</code>中的<code>name</code>对应。</p>

                <table class="config-table">
                    <thead>
                        <tr>
                            <th>字段名</th>
                            <th>类型</th>
                            <th>必选</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>links</code></td>
                            <td>array</td>
                            <td>是</td>
                            <td>链接数组，每个链接包含多个字段</td>
                        </tr>
                    </tbody>
                </table>

                <h4>链接字段说明</h4>
                <table class="config-table">
                    <thead>
                        <tr>
                            <th>字段名</th>
                            <th>类型</th>
                            <th>必选</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>name</code></td>
                            <td>string</td>
                            <td>是</td>
                            <td>链接名称，显示在卡片标题</td>
                        </tr>
                        <tr>
                            <td><code>url</code></td>
                            <td>string</td>
                            <td>是</td>
                            <td>链接地址，支持http/https网址或本地文件路径</td>
                        </tr>
                        <tr>
                            <td><code>description</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>链接描述，显示在卡片内容区</td>
                        </tr>
                        <tr>
                            <td><code>type</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>链接类型，用于分类显示和筛选</td>
                        </tr>
                        <tr>
                            <td><code>tag</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>链接标签，用于纵向标签显示和筛选功能</td>
                        </tr>
                    </tbody>
                </table>

                <h4>配置示例</h4>
                <div class="config-example">
                    <pre><code>{
        "普通分类": {
            "开发工具": {
                "links": [
                    {
                        "name": "Visual Studio Code",
                        "url": "https://code.visualstudio.com/",
                        "description": "轻量级强大的代码编辑器",
                        "type": "编辑器",
                        "tag": "IDE"
                    }
                ]
            }
        }
    }</code></pre>
                </div>
            </div>

            <div class="doc-section">
                <h3>📋 发布说明配置 (ReleaseNotes)</h3>
                <p>定义发布说明页面的内容。键名为发布类型名称。</p>

                <table class="config-table">
                    <thead>
                        <tr>
                            <th>字段名</th>
                            <th>类型</th>
                            <th>必选</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>icon</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>发布类型图标</td>
                        </tr>
                        <tr>
                            <td><code>type_description</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>发布类型描述</td>
                        </tr>
                        <tr>
                            <td><code>releases</code></td>
                            <td>array</td>
                            <td>是</td>
                            <td>发布版本数组</td>
                        </tr>
                    </tbody>
                </table>

                <h4>发布版本字段说明</h4>
                <table class="config-table">
                    <thead>
                        <tr>
                            <th>字段名</th>
                            <th>类型</th>
                            <th>必选</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>version</code></td>
                            <td>string</td>
                            <td>是</td>
                            <td>功能版本号</td>
                        </tr>
                        <tr>
                            <td><code>date</code></td>
                            <td>string</td>
                            <td>是</td>
                            <td>发布日期，格式：YYYY-MM-DD</td>
                        </tr>
                        <tr>
                            <td><code>main_version</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>主线版本号，显示为绿色标签</td>
                        </tr>
                        <tr>
                            <td><code>dev</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>开发人员</td>
                        </tr>
                        <tr>
                            <td><code>branch</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>代码分支</td>
                        </tr>
                        <tr>
                            <td><code>tag</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>Git标签</td>
                        </tr>
                        <tr>
                            <td><code>commit</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>提交哈希（自动截取前7位）</td>
                        </tr>
                        <tr>
                            <td><code>description</code></td>
                            <td>string</td>
                            <td>是</td>
                            <td>版本描述</td>
                        </tr>
                        <tr>
                            <td><code>details</code></td>
                            <td>array / string</td>
                            <td>否</td>
                            <td>详细功能列表，支持字符串（分号分隔）或数组格式</td>
                        </tr>
                    </tbody>
                </table>

                <h4>配置示例</h4>
                <div class="config-example">
                    <pre><code>{
        "ReleaseNotes": {
            "功能降级": {
                "icon": "⚠️",
                "type_description": "系统功能降级与容错处理",
                "releases": [
                    {
                        "version": "v1.2.0",
                        "date": "2024-01-15",
                        "main_version": "v2.1.0",
                        "dev": "张三",
                        "branch": "feature/graceful-degradation",
                        "tag": "v1.2.0-release",
                        "commit": "a1b2c3d4",
                        "description": "新增功能降级策略",
                        "details": ["降级检测机制", "状态监控", "资源释放"]
                    }
                ]
            }
        }
    }</code></pre>
                </div>
            </div>

            <div class="doc-section">
                <h3>📊 版本接口配置 (InterfaceMap)</h3>
                <p>定义版本接口页面的内容。键名为版本仓库名称。</p>

                <table class="config-table">
                    <thead>
                        <tr>
                            <th>字段名</th>
                            <th>类型</th>
                            <th>必选</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>description</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>版本仓库描述</td>
                        </tr>
                        <tr>
                            <td><code>branches</code></td>
                            <td>object</td>
                            <td>是</td>
                            <td>分支定义，键为分支ID，值为分支信息</td>
                        </tr>
                        <tr>
                            <td><code>versions</code></td>
                            <td>object</td>
                            <td>是</td>
                            <td>版本定义，键为版本ID，值为版本信息</td>
                        </tr>
                    </tbody>
                </table>

                <h4>版本字段说明</h4>
                <table class="config-table">
                    <thead>
                        <tr>
                            <th>字段名</th>
                            <th>类型</th>
                            <th>必选</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>branch</code></td>
                            <td>string</td>
                            <td>是</td>
                            <td>版本所属的分支ID</td>
                        </tr>
                        <tr>
                            <td><code>date</code></td>
                            <td>string</td>
                            <td>是</td>
                            <td>版本日期，格式：YYYY-MM-DD</td>
                        </tr>
                        <tr>
                            <td><code>description</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>版本的描述信息</td>
                        </tr>
                        <tr>
                            <td><code>interfaces</code></td>
                            <td>array / string</td>
                            <td>否</td>
                            <td>接口定义，支持多种格式</td>
                        </tr>
                        <tr>
                            <td><code>parent</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>父版本ID，用于版本继承关系</td>
                        </tr>
                        <tr>
                            <td><code>merge_target</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>合并目标版本，显示版本合并关系</td>
                        </tr>
                        <tr>
                            <td><code>tag</code></td>
                            <td>string</td>
                            <td>否</td>
                            <td>版本标签，自动识别状态（启用、弃用、移除、开发中、规划中）</td>
                        </tr>
                    </tbody>
                </table>

                <h4>配置示例</h4>
                <div class="config-example">
                    <pre><code>{
        "InterfaceMap": {
            "核心API演变": {
                "description": "核心API接口版本演变路线",
                "branches": {
                    "master": {
                        "name": "主分支",
                        "description": "主要开发分支",
                        "color": "#6366f1"
                    }
                },
                "versions": {
                    "v1.0.0": {
                        "branch": "master",
                        "date": "2023-10-01",
                        "description": "初始版本",
                        "interfaces": ["用户认证:v1.0", "数据查询:v1.0"],
                        "tag": "初始发版启用"
                    }
                }
            }
        }
    }</code></pre>
                </div>
            </div>

            <div class="doc-section">
                <h3>🔄 自动生成页面</h3>
                <p>以下页面类型无需额外配置，系统会自动生成内容：</p>

                <table class="config-table">
                    <thead>
                        <tr>
                            <th>页面类型</th>
                            <th>说明</th>
                            <th>导航配置示例</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>ConfigDocs</code></td>
                            <td>配置说明页面，显示本帮助文档</td>
                            <td><code>{"name": "配置说明", "icon": "📖", "type": "ConfigDocs"}</code></td>
                        </tr>
                        <tr>
                            <td><code>IconsReference</code></td>
                            <td>图标引用页面，提供可复制的emoji和SVG图标</td>
                            <td><code>{"name": "图标引用", "icon": "🎨", "type": "IconsReference"}</code></td>
                        </tr>
                    </tbody>
                </table>

                <div class="icon-tips">
                    <h4>💡 设计优势</h4>
                    <ul class="tips-list">
                        <li><strong>清晰分离</strong>：导航定义与内容数据分离，结构更清晰</li>
                        <li><strong>类型安全</strong>：通过<code>type</code>字段明确页面类型</li>
                        <li><strong>易于扩展</strong>：添加新页面类型只需增加新的<code>type</code>值</li>
                        <li><strong>统一管理</strong>：同类型数据集中存放，便于维护</li>
                        <li><strong>自动生成</strong>：部分页面无需配置，系统自动提供内容</li>
                    </ul>
                </div>
            </div>

            <div class="doc-section">
                <h3>📝 完整配置示例</h3>
                <div class="config-example">
                    <pre><code>{
        "site": {
            "title": "我的开发导航",
            "default_layout": "grid"
        },
        "categories": [
            {
                "name": "开发工具",
                "icon": "🛠️",
                "type": "普通分类"
            },
            {
                "name": "发布说明",
                "icon": "📋",
                "type": "ReleaseNotes"
            },
            {
                "name": "版本接口",
                "icon": "📊",
                "type": "InterfaceMap"
            },
            {
                "name": "配置说明",
                "icon": "📖",
                "type": "ConfigDocs"
            },
            {
                "name": "图标引用",
                "icon": "🎨",
                "type": "IconsReference"
            }
        ],
        "普通分类": {
            "开发工具": {
                "links": [
                    {
                        "name": "Visual Studio Code",
                        "url": "https://code.visualstudio.com/",
                        "description": "轻量级强大的代码编辑器",
                        "type": "编辑器",
                        "tag": "IDE"
                    }
                ]
            }
        },
        "ReleaseNotes": {
            "功能降级": {
                "icon": "⚠️",
                "type_description": "系统功能降级处理",
                "releases": [
                    {
                        "version": "v1.2.0",
                        "date": "2024-01-15",
                        "main_version": "v2.1.0",
                        "dev": "张三",
                        "branch": "feature/graceful-degradation",
                        "commit": "a1b2c3d4",
                        "description": "新增功能降级策略",
                        "details": ["降级检测机制", "状态监控", "资源释放"]
                    }
                ]
            }
        },
        "InterfaceMap": {
            "核心API演变": {
                "description": "核心API接口版本演变路线",
                "branches": {
                    "master": {
                        "name": "主分支",
                        "description": "主要开发分支",
                        "color": "#6366f1"
                    }
                },
                "versions": {
                    "v1.0.0": {
                        "branch": "master",
                        "date": "2023-10-01",
                        "description": "初始版本",
                        "interfaces": ["用户认证:v1.0", "数据查询:v1.0"],
                        "tag": "初始发版启用"
                    }
                }
            }
        }
    }</code></pre>
                </div>
            </div>
        </div>
        """

    def _get_svg_data(self):
        """获取SVG图标数据和分类 - 统一管理"""
        return {
            "icons": {
                # ============ 文件操作 ============
                "folder": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                    </svg>""",
                    "category": "文件操作",
                    "tags": ["folder", "directory", "文件夹"]
                },
                "file": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <line x1="16" y1="13" x2="8" y2="13"/>
                        <line x1="16" y1="17" x2="8" y2="17"/>
                        <polyline points="10 9 9 9 8 9"/>
                    </svg>""",
                    "category": "文件操作",
                    "tags": ["file", "document", "文件", "文档"]
                },
                "file-text": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <line x1="16" y1="13" x2="8" y2="13"/>
                        <line x1="16" y1="17" x2="8" y2="17"/>
                        <line x1="10" y1="9" x2="8" y2="9"/>
                    </svg>""",
                    "category": "文件操作",
                    "tags": ["file-text", "txt", "文本文件"]
                },
                "file-code": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <polyline points="16 13 12 9 16 5"/>
                        <polyline points="8 13 12 9 8 5"/>
                    </svg>""",
                    "category": "文件操作",
                    "tags": ["file-code", "代码文件", "源码"]
                },
                "save": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                        <polyline points="17 21 17 13 7 13 7 21"/>
                        <polyline points="7 3 7 8 15 8"/>
                    </svg>""",
                    "category": "文件操作",
                    "tags": ["save", "保存", "存储"]
                },
                "download": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7 10 12 15 17 10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                    </svg>""",
                    "category": "文件操作",
                    "tags": ["download", "下载"]
                },
                "upload": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="17 8 12 3 7 8"/>
                        <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>""",
                    "category": "文件操作",
                    "tags": ["upload", "上传"]
                },
                "copy": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                    </svg>""",
                    "category": "文件操作",
                    "tags": ["copy", "复制", "拷贝"]
                },
                "trash-2": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                        <line x1="10" y1="11" x2="10" y2="17"/>
                        <line x1="14" y1="11" x2="14" y2="17"/>
                    </svg>""",
                    "category": "文件操作",
                    "tags": ["trash", "delete", "删除", "垃圾桶"]
                },

                # ============ 开发工具 ============
                "code": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="16 18 22 12 16 6"/>
                        <polyline points="8 6 2 12 8 18"/>
                    </svg>""",
                    "category": "开发工具",
                    "tags": ["code", "编程", "代码", "开发"]
                },
                "terminal": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="4 17 10 11 4 5"/>
                        <line x1="12" y1="19" x2="20" y2="19"/>
                    </svg>""",
                    "category": "开发工具",
                    "tags": ["terminal", "终端", "命令行", "控制台"]
                },
                "cpu": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="4" y="4" width="16" height="16" rx="2" ry="2"/>
                        <rect x="9" y="9" width="6" height="6"/>
                        <line x1="9" y1="1" x2="9" y2="4"/>
                        <line x1="15" y1="1" x2="15" y2="4"/>
                        <line x1="9" y1="20" x2="9" y2="23"/>
                        <line x1="15" y1="20" x2="15" y2="23"/>
                        <line x1="20" y1="9" x2="23" y2="9"/>
                        <line x1="20" y1="14" x2="23" y2="14"/>
                        <line x1="1" y1="9" x2="4" y2="9"/>
                        <line x1="1" y1="14" x2="4" y2="14"/>
                    </svg>""",
                    "category": "开发工具",
                    "tags": ["cpu", "处理器", "计算"]
                },
                "server": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
                        <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
                        <line x1="6" y1="6" x2="6.01" y2="6"/>
                        <line x1="6" y1="18" x2="6.01" y2="18"/>
                    </svg>""",
                    "category": "开发工具",
                    "tags": ["server", "服务器", "服务"]
                },
                "database": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <ellipse cx="12" cy="5" rx="9" ry="3"/>
                        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                    </svg>""",
                    "category": "开发工具",
                    "tags": ["database", "数据库", "数据存储"]
                },
                "git-branch": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="6" y1="3" x2="6" y2="15"/>
                        <circle cx="18" cy="6" r="3"/>
                        <circle cx="6" cy="18" r="3"/>
                        <path d="M18 9a9 9 0 0 1-9 9"/>
                    </svg>""",
                    "category": "开发工具",
                    "tags": ["git", "branch", "分支", "版本控制"]
                },
                "git-merge": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="18" cy="18" r="3"/>
                        <circle cx="6" cy="6" r="3"/>
                        <path d="M6 21V9a9 9 0 0 0 9 9"/>
                    </svg>""",
                    "category": "开发工具",
                    "tags": ["git", "merge", "合并", "版本控制"]
                },

                # ============ 状态指示 ============
                "check-circle": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                        <polyline points="22 4 12 14.01 9 11.01"/>
                    </svg>""",
                    "category": "状态指示",
                    "tags": ["check", "success", "成功", "完成", "正确"]
                },
                "alert-circle": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>""",
                    "category": "状态指示",
                    "tags": ["alert", "warning", "警告", "注意"]
                },
                "x-circle": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="15" y1="9" x2="9" y2="15"/>
                        <line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>""",
                    "category": "状态指示",
                    "tags": ["x", "close", "error", "错误", "关闭", "取消"]
                },
                "info": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="16" x2="12" y2="12"/>
                        <line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>""",
                    "category": "状态指示",
                    "tags": ["info", "information", "信息", "详情"]
                },
                "help-circle": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                        <line x1="12" y1="17" x2="12.01" y2="17"/>
                    </svg>""",
                    "category": "状态指示",
                    "tags": ["help", "question", "帮助", "疑问", "问题"]
                },
                "plus-circle": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="16"/>
                        <line x1="8" y1="12" x2="16" y2="12"/>
                    </svg>""",
                    "category": "状态指示",
                    "tags": ["plus", "add", "添加", "新建", "增加"]
                },
                "minus-circle": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="8" y1="12" x2="16" y2="12"/>
                    </svg>""",
                    "category": "状态指示",
                    "tags": ["minus", "remove", "删除", "减少", "移除"]
                },

                # ============ 网络通信 ============
                "globe": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="2" y1="12" x2="22" y2="12"/>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                    </svg>""",
                    "category": "网络通信",
                    "tags": ["globe", "world", "地球", "网络", "互联网"]
                },
                "wifi": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M5 12.55a11 11 0 0 1 14.08 0"/>
                        <path d="M1.42 9a16 16 0 0 1 21.16 0"/>
                        <path d="M8.53 16.11a6 6 0 0 1 6.95 0"/>
                        <line x1="12" y1="20" x2="12.01" y2="20"/>
                    </svg>""",
                    "category": "网络通信",
                    "tags": ["wifi", "无线", "网络", "连接"]
                },
                "bluetooth": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6.5 6.5 17.5 17.5 12 23 12 1 17.5 6.5 6.5 17.5"/>
                    </svg>""",
                    "category": "网络通信",
                    "tags": ["bluetooth", "蓝牙", "无线"]
                },
                "link": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                        <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                    </svg>""",
                    "category": "网络通信",
                    "tags": ["link", "连接", "链接", "网址"]
                },

                # ============ 媒体图标 ============
                "image": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                        <circle cx="8.5" cy="8.5" r="1.5"/>
                        <polyline points="21 15 16 10 5 21"/>
                    </svg>""",
                    "category": "媒体图标",
                    "tags": ["image", "picture", "图片", "照片", "图像"]
                },
                "video": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="23 7 16 12 23 17 23 7"/>
                        <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                    </svg>""",
                    "category": "媒体图标",
                    "tags": ["video", "视频", "影片", "播放"]
                },
                "music": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M9 18V5l12-2v13"/>
                        <circle cx="6" cy="18" r="3"/>
                        <circle cx="18" cy="16" r="3"/>
                    </svg>""",
                    "category": "媒体图标",
                    "tags": ["music", "音乐", "音频", "声音"]
                },

                # ============ 时间相关 ============
                "calendar": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <line x1="16" y1="2" x2="16" y2="6"/>
                        <line x1="8" y1="2" x2="8" y2="6"/>
                        <line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>""",
                    "category": "时间相关",
                    "tags": ["calendar", "日期", "日历", "日程"]
                },
                "clock": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12 6 12 12 16 14"/>
                    </svg>""",
                    "category": "时间相关",
                    "tags": ["clock", "时间", "时钟", "计时"]
                },
                "watch": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="7"/>
                        <polyline points="12 9 12 12 13.5 13.5"/>
                        <path d="M16.51 17.35l-.35 3.83a2 2 0 0 1-2 1.82H9.83a2 2 0 0 1-2-1.82l-.35-3.83m.01-10.7l.35-3.83A2 2 0 0 1 9.83 1h4.35a2 2 0 0 1 2 1.82l.35 3.83"/>
                    </svg>""",
                    "category": "时间相关",
                    "tags": ["watch", "手表", "计时器"]
                },

                # ============ 常用图标 ============
                "home": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                        <polyline points="9 22 9 12 15 12 15 22"/>
                    </svg>""",
                    "category": "常用图标",
                    "tags": ["home", "主页", "首页", "家"]
                },
                "settings": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="3"/>
                        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                    </svg>""",
                    "category": "常用图标",
                    "tags": ["settings", "设置", "配置", "偏好"]
                },
                "edit": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>""",
                    "category": "常用图标",
                    "tags": ["edit", "编辑", "修改", "书写"]
                },
                "search": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="11" cy="11" r="8"/>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>""",
                    "category": "常用图标",
                    "tags": ["search", "搜索", "查找", "查询"]
                },

                # ============ 用户界面 ============
                "user": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                        <circle cx="12" cy="7" r="4"/>
                    </svg>""",
                    "category": "用户界面",
                    "tags": ["user", "用户", "个人", "账户"]
                },
                "users": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>""",
                    "category": "用户界面",
                    "tags": ["users", "用户组", "团队", "成员"]
                },
                "bell": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                    </svg>""",
                    "category": "用户界面",
                    "tags": ["bell", "通知", "提醒", "铃铛"]
                },

                # ============ 导航方向 ============
                "chevron-up": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="18 15 12 9 6 15"/>
                    </svg>""",
                    "category": "导航方向",
                    "tags": ["chevron-up", "向上", "展开", "收起"]
                },
                "chevron-down": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6 9 12 15 18 9"/>
                    </svg>""",
                    "category": "导航方向",
                    "tags": ["chevron-down", "向下", "收起", "展开"]
                },
                "chevron-left": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="15 18 9 12 15 6"/>
                    </svg>""",
                    "category": "导航方向",
                    "tags": ["chevron-left", "向左", "后退", "返回"]
                },
                "chevron-right": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="9 18 15 12 9 6"/>
                    </svg>""",
                    "category": "导航方向",
                    "tags": ["chevron-right", "向右", "前进", "下一步"]
                },

                # ============ Jenkins/CI/CD ============
                "jenkins": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                        <circle cx="8.5" cy="8.5" r="1.5"/>
                        <circle cx="15.5" cy="8.5" r="1.5"/>
                        <line x1="8" y1="14" x2="16" y2="14"/>
                        <line x1="8" y1="17" x2="16" y2="17"/>
                    </svg>""",
                    "category": "Jenkins/CI/CD",
                    "tags": ["jenkins", "ci", "cd", "持续集成", "自动化"]
                },
                "package": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12.89 1.45l8 4A2 2 0 0 1 22 7.24v9.53a2 2 0 0 1-1.11 1.79l-8 4a2 2 0 0 1-1.79 0l-8-4a2 2 0 0 1-1.1-1.8V7.24a2 2 0 0 1 1.11-1.79l8-4a2 2 0 0 1 1.78 0z"/>
                        <polyline points="2.32 6.16 12 11 21.68 6.16"/>
                        <line x1="12" y1="22.76" x2="12" y2="11"/>
                    </svg>""",
                    "category": "Jenkins/CI/CD",
                    "tags": ["package", "打包", "发布", "部署"]
                },
                "truck": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="1" y="3" width="15" height="13"/>
                        <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/>
                        <circle cx="5.5" cy="18.5" r="2.5"/>
                        <circle cx="18.5" cy="18.5" r="2.5"/>
                    </svg>""",
                    "category": "Jenkins/CI/CD",
                    "tags": ["truck", "运输", "交付", "部署"]
                },

                # ============ 嵌入式开发 ============
                "microcontroller": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="4" y="4" width="16" height="16" rx="2"/>
                        <rect x="9" y="9" width="6" height="6"/>
                        <line x1="9" y1="1" x2="9" y2="4"/>
                        <line x1="15" y1="1" x2="15" y2="4"/>
                        <line x1="9" y1="20" x2="9" y2="23"/>
                        <line x1="15" y1="20" x2="15" y2="23"/>
                        <line x1="20" y1="9" x2="23" y2="9"/>
                        <line x1="20" y1="14" x2="23" y2="14"/>
                        <line x1="1" y1="9" x2="4" y2="9"/>
                        <line x1="1" y1="14" x2="4" y2="14"/>
                    </svg>""",
                    "category": "嵌入式开发",
                    "tags": ["microcontroller", "单片机", "微控制器", "嵌入式"]
                },
                "sensor": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 16.2A4.5 4.5 0 0 0 17.5 8h-1.8A7 7 0 1 0 4 16.2"/>
                        <path d="M9.5 11.5a2.5 2.5 0 0 1 0 5"/>
                        <path d="M12.5 8.5a5.5 5.5 0 0 1 0 11"/>
                    </svg>""",
                    "category": "嵌入式开发",
                    "tags": ["sensor", "传感器", "检测", "感应"]
                },
                "battery": {
                    "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="1" y="6" width="18" height="12" rx="2" ry="2"/>
                        <line x1="23" y1="13" x2="23" y2="11"/>
                    </svg>""",
                    "category": "嵌入式开发",
                    "tags": ["battery", "电池", "电量", "电源"]
                },
            },

            # 自动生成的分类索引（无需手动维护）
            "categories": None  # 这里会在初始化时自动生成
        }

    # 在你的类中添加辅助方法
    def _init_svg_data(self):
        """初始化SVG数据，自动生成分类索引"""
        svg_data = self._get_svg_data()

        # 自动生成分类索引
        categories = {}
        for icon_name, icon_data in svg_data["icons"].items():
            category = icon_data["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(icon_name)

        svg_data["categories"] = categories
        return svg_data

    def _get_svg_icons(self):
        """获取所有SVG图标（兼容原有接口）"""
        svg_data = self._init_svg_data()
        return {name: data["svg"] for name, data in svg_data["icons"].items()}

    def _get_svg_categories(self):
        """获取SVG分类（兼容原有接口）"""
        svg_data = self._init_svg_data()
        return svg_data["categories"]

    def _get_icon_info(self, icon_name):
        """获取图标详细信息"""
        svg_data = self._init_svg_data()
        if icon_name in svg_data["icons"]:
            return svg_data["icons"][icon_name]
        return None

    def _get_icons_by_category(self, category):
        """按分类获取图标"""
        svg_data = self._init_svg_data()
        icons = {}
        for icon_name in svg_data["categories"].get(category, []):
            if icon_name in svg_data["icons"]:
                icons[icon_name] = svg_data["icons"][icon_name]["svg"]
        return icons

    def _search_icons(self, keyword):
        """搜索图标（按名称或标签）"""
        svg_data = self._init_svg_data()
        results = {}
        keyword_lower = keyword.lower()

        for icon_name, icon_data in svg_data["icons"].items():
            # 匹配图标名称
            if keyword_lower in icon_name.lower():
                results[icon_name] = icon_data["svg"]
                continue

            # 匹配标签
            if any(keyword_lower in tag.lower() for tag in icon_data["tags"]):
                results[icon_name] = icon_data["svg"]

        return results

    def _render_icon(self, icon_value):
        """根据icon值渲染图标，支持emoji和SVG ID

        Args:
            icon_value: 图标值，可以是emoji字符串或SVG ID

        Returns:
            渲染后的HTML字符串
        """
        if not icon_value:
            return "📁"  # 默认图标

        # 获取SVG图标库
        svg_icons = self._get_svg_icons()

        # 检查是否是SVG ID
        if icon_value in svg_icons:
            svg_code = svg_icons[icon_value]
            # 返回SVG代码，添加CSS类名以便控制样式
            return f'<span class="svg-icon">{svg_code}</span>'
        else:
            # 否则作为emoji显示
            return icon_value

    def _render_icon_simple(self, icon_value):
        """简化的图标渲染"""
        if not icon_value:
            return "📁"

        svg_icons = self._get_svg_icons()

        if icon_value in svg_icons:
            # 如果是SVG ID，返回SVG代码
            return f'<span class="svg-icon">{svg_icons[icon_value]}</span>'
        else:
            # 否则作为emoji显示
            return icon_value

    def _escape_svg(self, svg):
        """转义SVG中的特殊字符"""
        if not svg:
            return ""
        # 移除换行，压缩多个空格为单个空格
        svg = ' '.join(svg.split())
        # 转义HTML特殊字符
        svg = svg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
        return svg

    def _generate_icons_reference(self):
        """生成图标引用页面内容 - 简化版"""

        # Emoji 分类和示例 - 显示所有emoji
        emoji_categories = [
            {
                "name": "常用图标",
                "emojis": ["📁", "🛠️", "📚", "💻", "🔧", "📊", "📋", "⚠️", "🐛", "🚀", "✨", "⚡", "🔒", "🔑", "🔍", "📈", "📉", "🎯",
                           "🎨", "📖"]
            },
            {
                "name": "开发工具",
                "emojis": ["💾", "📝", "🔍", "📐", "🧮", "🔬", "⚙️", "🔩", "🔨", "🪛", "🔧", "💻", "📱", "🖥️", "🖨️", "📡", "🔌", "🔋",
                           "💡", "🧰"]
            },
            {
                "name": "文件类型",
                "emojis": ["📄", "📑", "📖", "📓", "📒", "📕", "📗", "📘", "📙", "🗂️", "📁", "📂", "🗃️", "🗄️", "📇", "📋", "📊", "📈",
                           "📉", "🗒️"]
            },
            {
                "name": "状态指示",
                "emojis": ["✅", "❌", "⚠️", "⏳", "📈", "📉", "🔴", "🟡", "🟢", "🔵", "🟣", "🟠", "⚫", "⚪", "🟤", "⭕", "❓", "❗",
                           "💡", "🔔"]
            },
            {
                "name": "人物角色",
                "emojis": ["👤", "👥", "👨‍💻", "👩‍💻", "👨‍🔬", "👩‍🔬", "👨‍🎓", "👩‍🎓", "👨‍🏫", "👩‍🏫", "👨‍🔧", "👩‍🔧", "👨‍🚀",
                           "👩‍🚀", "👨‍✈️", "👩‍✈️", "👨‍🚒", "👩‍🚒", "🕵️‍♂️", "🕵️‍♀️"]
            },
            {
                "name": "版本控制",
                "emojis": ["🌿", "🔀", "📦", "🏷️", "🔗", "📎", "📌", "📍", "🎯", "🎪", "🔖", "📋", "📄", "📑", "🗂️", "🗃️", "📊", "📈",
                           "📉", "🧾"]
            },
            {
                "name": "操作按钮",
                "emojis": ["📥", "📤", "🗑️", "✏️", "🔍", "🔎", "➕", "➖", "✖️", "➗", "🔄", "⏪", "⏩", "⏸️", "⏹️", "⏺️", "⏏️",
                           "🔀", "🔁", "🔂"]
            }
        ]

        # 生成Emoji部分
        emoji_sections = ""
        for category in emoji_categories:
            emoji_grid = ""
            for emoji in category["emojis"]:
                # 简化处理，避免复杂的ord()调用
                char_code = f"U+{ord(emoji[0]):04X}" if emoji else "U+0000"

                emoji_grid += f"""
                <div class="icon-item emoji-item" data-icon="{emoji}" onclick="copyIcon('{emoji}')">
                    <div class="icon-display">{emoji}</div>
                    <div class="icon-code">{char_code}</div>
                </div>
                """

            emoji_sections += f"""
            <div class="icon-category">
                <h4>{category["name"]}</h4>
                <div class="icon-grid">
                    {emoji_grid}
                </div>
            </div>
            """

        # SVG图标部分 - 简化为按分类显示
        # 1. 获取所有图标（兼容原有代码）
        svg_icons = self._get_svg_icons()
        # 2. 获取分类（兼容原有代码）
        svg_categories = self._get_svg_categories()
        # 3. 获取图标详细信息
        icon_info = self._get_icon_info("folder")
        # 返回: {"svg": "...", "category": "文件操作", "tags": [...]}
        # 4. 按分类获取图标
        file_icons = self._get_icons_by_category("文件操作")
        # 5. 搜索图标
        search_results = self._search_icons("代码")
        # 搜索"代码"会返回: code, file-code等

        svg_sections = ""
        for category_name, icon_ids in svg_categories.items():
            svg_grid = ""
            for icon_id in icon_ids:
                if icon_id in svg_icons:
                    svg_code = svg_icons[icon_id]
                    svg_grid += f"""
                    <div class="icon-item svg-item" data-icon-id="{icon_id}" onclick="copyIcon('{icon_id}')">
                        <div class="icon-display svg-display">
                            {svg_code}
                        </div>
                        <div class="icon-id">{icon_id}</div>
                    </div>
                    """

            svg_sections += f"""
            <div class="icon-category">
                <h4>{category_name}</h4>
                <div class="icon-grid svg-grid">
                    {svg_grid}
                </div>
            </div>
            """

        return f"""
        <div class="docs-container">
            <div class="doc-section">
                <h3>🎨 图标引用</h3>
                <p>本页面提供可在配置文件中使用的图标资源，支持点击复制。</p>

                <div class="icon-tips">
                    <h4>💡 使用提示</h4>
                    <ul class="tips-list">
                        <li><strong>Emoji图标</strong>：点击复制emoji字符，直接粘贴到JSON的<code>"icon"</code>字段</li>
                        <li><strong>SVG图标</strong>：点击复制图标ID（如：folder），使用ID作为<code>"icon"</code>字段值</li>
                        <li>系统会自动识别并渲染对应的图标</li>
                        <li>所有图标均兼容主流系统和浏览器</li>
                    </ul>
                </div>
            </div>

            <div class="doc-section">
                <h3>😀 Emoji 图标</h3>
                <p>Unicode Emoji，直接使用字符串格式。</p>

                {emoji_sections}
            </div>

            <div class="doc-section">
                <h3>🎨 SVG 矢量图标</h3>
                <p>使用Lucide图标集，点击复制图标ID。</p>

                {svg_sections}

                <h4>使用示例</h4>
                <div class="config-example">
                    <pre><code>{{
        "categories": [
            {{
                "name": "开发工具",
                "icon": "code",  // ← 使用SVG ID
                "type": "普通分类"
            }},
            {{
                "name": "文档管理", 
                "icon": "📁",  // ← 使用emoji
                "type": "普通分类"
            }}
        ]
    }}</code></pre>
                </div>
            </div>
        </div>
        """

    def generate_html(self, output_file="soft_navigation.html"):
        """生成柔和风格导航网站"""

        # 生成时间
        generated_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 生成分类导航HTML
        nav_items = ""
        category_sections = ""

        # 首先生成所有分类的导航项
        category_list = list(self.categories.items())
        for i, (category_name, category_data) in enumerate(category_list):
            # 获取分类图标
            category_icon = self._render_icon(category_data['icon'])
            # 导航项
            active_class = "active" if i == 0 else ""
            nav_items += f"""
                <button class="nav-item {active_class}" data-category="{category_name}">
                    <i>{category_icon }</i>
                    {category_name}
                </button>
            """

        # 接着生成所有分类的内容区域
        for i, (category_name, category_data) in enumerate(category_list):
            # 分类内容区域
            active_section = "active" if i == 0 else ""
            category_type = category_data.get('type', '普通分类')

            if category_type == 'ReleaseNotes':
                # 发布说明页面
                category_sections += self._generate_release_notes_section(category_name, active_section)

            elif category_type == 'InterfaceMap':
                # 版本接口页面
                category_sections += self._generate_interface_map_section(category_name, active_section)

            elif category_type == 'ConfigDocs':
                # 配置说明页面
                category_sections += self._generate_config_docs_section(category_name, active_section)

            elif category_type == 'IconsReference':
                # 图标引用页面
                category_sections += self._generate_icons_reference_section(category_name, active_section)

            else:
                # 普通分类页面
                category_sections += self._generate_normal_category_section(category_name, category_data,
                                                                            active_section)

        # 使用说明
        usage_note = """
        <div class="usage-help">?</div>
        <div class="usage-tooltip" id="usageTooltip">
            <h3>💡 使用提示</h3>
            <ul>
                <li><strong>本地文件夹</strong>：绿色按钮表示本地文件夹链接</li>
                <li><strong>复制路径</strong>：点击 📋 按钮复制文件夹路径</li>
                <li><strong>打开方式</strong>：右键点击"打开"按钮选择不同方式</li>
                <li><strong>标签筛选</strong>：点击标签筛选特定类型链接</li>
                <li><strong>发布说明</strong>：点击左侧卡片查看时间轴</li>
                <li><strong>版本仓库</strong>：支持统一视图和分组视图切换</li>
            </ul>
        </div>
        """

        # 统计总链接数
        total_links = sum(len(cat["links"]) for cat in self.categories.values() if cat.get('type') == '普通分类')
        total_release_notes = sum(len(releases) for releases in self.release_notes.values())
        total_interface_routes = len(self.interface_routes.interface_routes)

        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title}</title>
            <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%236366f1'/%3E%3Cstop offset='100%25' stop-color='%238b5cf6'/%3E%3C/linearGradient%3E%3C/defs%3E%3Ccircle cx='50' cy='50' r='45' fill='url(%23g)'/%3E%3Ccircle cx='50' cy='50' r='40' fill='white'/%3E%3Cpath d='M50 25 L62 45 L50 55 L38 45 Z' fill='url(%23g)'/%3E%3Ccircle cx='50' cy='50' r='5' fill='%236366f1'/%3E%3C/svg%3E">
            <style>{self.css_style}</style>
        </head>
        <body>
            <div class="sidebar">
                <div class="logo">
                    <h1>{self.title}</h1>
                    <p>简洁 · 高效 · 实用</p>
                </div>
                <nav class="nav-categories">
                    {nav_items}
                </nav>
            </div>

            <div class="main-content">
                {category_sections}

                {usage_note}

                <div class="footer">
                    <p class="generator-info">由 {self.generator_info} 生成于 {generated_time}</p>
                    <p class="developer-info"> ✍ @FastXTeam/wanqiang.liu | 📧 zerocirculation@gmail.com | ©All CopyRights Reserved. </p>
                </div>
            </div>

            <!-- 固定在右下角的统计信息 -->
            <div class="stats">
                {len([c for c in self.categories.values() if c.get('type') == '普通分类'])} 分类 · {total_links} 链接 · {len(self.release_notes)} 发布类型 · {total_release_notes} 版本 · {total_interface_routes} 版本仓库
            </div>

            <!-- 通知消息 -->
            <div id="notification" class="notification"></div>

            <!-- 本地文件夹选项模态框 -->
            <div id="folderOptionsModal" class="modal-overlay">
                <div class="modal">
                    <h3>打开本地文件夹</h3>
                    <p id="modalFolderPath"></p>
                    <div class="modal-actions">
                        <button class="modal-btn secondary" id="modalCopyPath">复制路径</button>
                        <button class="modal-btn primary" id="modalOpenDefault">默认方式打开</button>
                        <button class="modal-btn secondary" id="modalCancel">取消</button>
                    </div>
                </div>
            </div>
            
            <!-- 使用内联 JavaScript -->
            <script>
            {self.js_script}
            </script>
        </body>
        </html>
        """

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # 统计不同类型页面的数量
        normal_categories = len([c for c in self.categories.values() if c.get('type') == '普通分类'])
        special_categories = len([c for c in self.categories.values() if c.get('type') != '普通分类'])

        print(f"✅ 柔和风格导航网站已生成: {output_file}")
        print(f"📁 包含 {normal_categories} 个普通分类, {special_categories} 个特殊页面")
        print(f"🔗 总共 {total_links} 个链接")
        print(f"📋 包含 {len(self.release_notes)} 个发布类型，{total_release_notes} 个版本")
        print(f"📊 包含 {total_interface_routes} 个版本仓库")
        print(f"🕒 生成时间: {generated_time}")
        print(f"📊 默认布局: {self.default_layout}")


def parse_json_config(config_file):
    """解析 JSON 配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON配置文件格式错误: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ 配置文件不存在: {config_file}")
        sys.exit(1)

    # 获取网站标题和默认布局
    site_config = config.get('site', {})
    title = site_config.get('title', '嵌入式开发中心')
    default_layout = site_config.get('default_layout', 'list')

    # 创建生成器实例
    generator = SoftNavGenerator(title, default_layout)

    # 解析分类导航
    categories = config.get('categories', [])

    # 先解析所有分类（包括特殊分类）
    for category in categories:
        category_name = category.get('name', '')
        icon = category.get('icon', '📁')
        category_type = category.get('type', '普通分类')

        # 添加分类到导航
        if category_type == '普通分类':
            # 解析普通分类的链接
            category_data = config.get('普通分类', {}).get(category_name, {})
            links = category_data.get('links', [])

            # 转换链接格式为内部使用的格式
            links_list = []
            for link in links:
                name = link.get('name', '')
                url = link.get('url', '')
                description = link.get('description', '')
                link_type = link.get('type', '网站')
                tag = link.get('tag', '')
                links_list.append([name, url, description, link_type, tag])

            generator.add_category(category_name, links_list, icon, category_type)

        else:
            # 特殊分类（只有导航项，内容由对应的类型提供）
            generator.add_category(category_name, [], icon, category_type)

    # 解析发布说明
    release_notes_config = config.get('ReleaseNotes', {})
    for release_type, release_data in release_notes_config.items():
        icon = release_data.get('icon', '📋')
        type_description = release_data.get('type_description', '')
        releases = release_data.get('releases', [])

        # 处理每个发布版本的details字段
        processed_releases = []
        for release in releases:
            processed_release = release.copy()

            # 确保每个release都有图标和类型描述
            processed_release['icon'] = icon
            processed_release['type_description'] = type_description

            # 处理details字段
            details = release.get('details', '')
            if isinstance(details, str) and details:
                processed_release['details'] = [d.strip() for d in details.split(';') if d.strip()]
            elif isinstance(details, list):
                processed_release['details'] = details
            else:
                processed_release['details'] = ''

            processed_releases.append(processed_release)

        generator.add_release_note(release_type, processed_releases)

    # 解析版本接口
    interface_routes_config = config.get('InterfaceMap', {})
    for route_name, route_data in interface_routes_config.items():
        description = route_data.get('description', '接口版本演变路线')
        branches = route_data.get('branches', {})
        versions = route_data.get('versions', {})

        # 处理版本中的interfaces字段
        processed_versions = {}
        for version_id, version_data in versions.items():
            processed_version = version_data.copy()

            # 处理interfaces字段：统一转换为字符串格式
            interfaces = version_data.get('interfaces', '')
            if isinstance(interfaces, list):
                # 将列表转换为字符串格式
                interface_strs = []
                for item in interfaces:
                    if isinstance(item, str):
                        interface_strs.append(item.strip())
                    elif isinstance(item, dict) and 'name' in item:
                        version = item.get('version', 'v1.0')
                        interface_strs.append(f"{item['name']}:{version}")
                    else:
                        interface_strs.append(str(item))
                processed_version['interfaces'] = ', '.join(interface_strs)
            else:
                # 已经是字符串或空值
                processed_version['interfaces'] = str(interfaces) if interfaces else ''

            processed_versions[version_id] = processed_version

        route_config = {
            'branches': branches,
            'versions': processed_versions,
            'description': description
        }
        generator.interface_routes.add_interface_route(route_name, route_config)

    return generator


def create_sample_json():
    """创建示例 JSON 配置文件"""
    sample_content = {
        "site": {
            "title": "嵌入式开发中心",
            "default_layout": "list"
        },
        "categories": [
            {
                "name": "开发工具",
                "icon": "🛠️",
                "type": "普通分类"
            },
            {
                "name": "发布说明",
                "icon": "📋",
                "type": "ReleaseNotes"
            }
        ],
        "普通分类": {
            "开发工具": {
                "links": [
                    {
                        "name": "Visual Studio Code",
                        "url": "https://code.visualstudio.com/",
                        "description": "轻量级强大的代码编辑器",
                        "type": "编辑器",
                        "tag": "IDE"
                    }
                ]
            }
        },
        "ReleaseNotes": {
            "功能降级": {
                "icon": "⚠️",
                "type_description": "系统功能降级与容错处理",
                "releases": [
                    {
                        "version": "v1.2.0",
                        "date": "2024-01-15",
                        "main_version": "v2.1.0",
                        "dev": "张三",
                        "branch": "feature/graceful-degradation",
                        "commit": "a1b2c3d4",
                        "description": "新增功能降级策略",
                        "details": ["降级检测机制", "状态监控", "资源释放"]
                    }
                ]
            }
        },
        "InterfaceMap": {
            "核心API演变": {
                "description": "核心API接口版本演变路线",
                "branches": {
                    "master": {
                        "name": "主分支",
                        "description": "主要开发分支",
                        "color": "#6366f1"
                    }
                },
                "versions": {
                    "v1.0.0": {
                        "branch": "master",
                        "date": "2023-10-01",
                        "description": "初始版本",
                        "interfaces": ["用户认证:v1.0", "数据查询:v1.0"],
                        "tag": "初始发版启用"
                    }
                }
            }
        }
    }

    with open('config_sample.json', 'w', encoding='utf-8') as f:
        json.dump(sample_content, f, ensure_ascii=False, indent=2)

    print("✅ 示例配置文件已生成: config_sample.json")


def main():
    """主函数 - 命令行参数版本"""
    parser = argparse.ArgumentParser(description='生成导航网站')
    parser.add_argument('--config', type=str, required=True, help='JSON 配置文件路径')
    parser.add_argument('--output', type=str, default='navigation.html', help='输出 HTML 文件路径')
    parser.add_argument('--create-sample', action='store_true', help='创建示例配置文件')

    args = parser.parse_args()

    if args.create_sample:
        create_sample_json()
        return

    # 检查配置文件是否存在
    if not os.path.exists(args.config):
        print(f"❌ 配置文件不存在: {args.config}")
        print("📝 正在创建示例配置文件...")
        create_sample_json()
        print("💡 请编辑 config_sample.json 并根据需要重命名")
        return

    try:
        # 解析配置文件并生成网站
        generator = parse_json_config(args.config)
        generator.generate_html(args.output)
    except Exception as e:
        print(f"❌ 生成网站时出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()