#!/bin/bash
# Claude in Chromeで開いたタブグループを閉じるスクリプト
# Stopフックから呼び出される

osascript <<'APPLESCRIPT'
tell application "Google Chrome"
    repeat with w in every window
        set tabGroups to {}
        set tabsToClose to {}

        -- タブグループに属するタブを検出して閉じる
        -- Claude in Chromeのグループは "Claude" という名前のタブグループ
        set tabCount to count of tabs of w
        repeat with i from tabCount to 1 by -1
            set t to tab i of w
            set tabURL to URL of t
            set tabTitle to title of t
            -- Claude in Chromeが作成したタブを検出
            -- 新しいタブ or Claude関連のグループタブ
            if tabURL starts with "chrome://newtab" then
                close t
            end if
        end repeat
    end repeat
end tell

-- JavaScriptでタブグループを閉じる（Chrome拡張のグループ）
tell application "Google Chrome"
    repeat with w in every window
        try
            execute front tab of w javascript "
                (async () => {
                    const groups = await chrome.tabGroups.query({});
                    for (const group of groups) {
                        if (group.title && group.title.includes('Claude')) {
                            const tabs = await chrome.tabs.query({groupId: group.id});
                            for (const tab of tabs) {
                                await chrome.tabs.remove(tab.id);
                            }
                        }
                    }
                })();
            "
        end try
    end repeat
end tell
APPLESCRIPT
