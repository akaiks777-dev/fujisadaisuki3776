#!/bin/bash
OUTPUT=$(osascript <<'APPLESCRIPT_EOF'
set todayDate to current date
set todayDate to (todayDate - (time of todayDate))
set weekEnd to todayDate + 7 * days
set monthEnd to todayDate + 30 * days

set todayStr to ""
set weekStr to ""
set monthStr to ""
set todayCount to 0
set weekCount to 0
set monthCount to 0

tell application "Calendar"
    repeat with c in calendars
        try
            set calName to name of c
            if writable of c is true and calName does not contain "祝日" and calName does not contain "Holiday" and calName does not contain "誕生日" and calName does not contain "提案" then
                set evList to (every event of c whose start date ≥ todayDate and start date < monthEnd)
                repeat with ev in evList
                    set evTitle to summary of ev
                    set evStart to start date of ev
                    if evStart < (todayDate + 1 * days) then
                        set todayStr to todayStr & return & "  • " & (time string of evStart) & " " & evTitle
                        set todayCount to todayCount + 1
                    else if evStart < weekEnd then
                        set weekStr to weekStr & return & "  • " & (short date string of evStart) & " " & evTitle
                        set weekCount to weekCount + 1
                    else
                        set monthStr to monthStr & return & "  • " & (short date string of evStart) & " " & evTitle
                        set monthCount to monthCount + 1
                    end if
                end repeat
            end if
        end try
    end repeat
end tell

set output to "【本日】" & todayCount & "件" & todayStr & return & return & "【今週】" & weekCount & "件" & weekStr & return & return & "【今月】" & monthCount & "件" & monthStr
return output
APPLESCRIPT_EOF
)

osascript -e "display dialog \"$OUTPUT\" with title \"📅 本日のスケジュール\" buttons {\"OK\"} default button 1"
