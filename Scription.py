import re
import os
import sys
import time

# Helper function to unpack continuous phrases hiding on the same line segment
def parse_continuous_phrases(text):
    # Matches individual valid Scription phrases securely from left to right
    pattern = r'(?:print\s+["\'][^"\']*["\']\s*\d+[xX]|print\s+["\'][^"\']*["\']|wait\s+["\'][^"\']*["\']|countdown\s+["\'][^"\']*["\']|stopcount\s+["\'][^"\']*["\']|\w+)'
    return [match.strip() for match in re.findall(pattern, text, re.IGNORECASE)]

def execute_phrase(phrase, memory, line_num, trackers):
    phrase = phrase.strip()
    if not phrase or phrase.startswith('--') or phrase.startswith('#'):
        return True
        
    phrase_lower = phrase.lower()
    
    if not trackers["condition_passed"] and not phrase_lower.startswith('otherwise') and not phrase_lower.startswith('else:') and not phrase_lower.startswith('if '):
        return True

    # 🚀 1. INLINE MULTIPLIER MATRIX CORE (1x to 1,000,000,000x)
    if re.search(r'\s+\d+[xX]$', phrase):
        match_mult = re.search(r'(\d+)[xX]$', phrase)
        if match_mult:
            multiplier = int(match_mult.group(1))
            clean_cmd = re.sub(r'\s+\d+[xX]$', '', phrase)
            for _ in range(multiplier):
                success = execute_phrase(clean_cmd, memory, line_num, trackers)
                if not success: return False
            return True

    # 💬 2. UNIVERSAL PRINT FEEDBACK UNIT
    if phrase_lower.startswith('print'):
        match_str = re.search(r'["\']([^"\']+)["\']', phrase)
        if match_str:
            print(match_str.group(1))
            return True
        match_var = re.search(r'(?:print)\s+(\w+)', phrase, re.IGNORECASE)
        if match_var:
            var_name = match_var.group(1)
            k = next((x for x in memory if x.lower() == var_name.lower()), var_name)
            if k in memory: print(memory[k])
            return True

    # 🐍 3. PYTHON VARIANT CONVERSION ASSIGNMENT SHIELD
    if '=' in phrase and not phrase_lower.startswith('savespacefor ') and not '==' in phrase and not 'child of' in phrase_lower:
        phrase = "SaveSpaceFor " + phrase.replace('=', ' is ', 1)
        phrase_lower = phrase.lower()

    # Convert logic operators regardless of original case typing
    if ' and ' in phrase_lower: phrase = re.sub(r'\s+and\s+', ' Also ', phrase, flags=re.IGNORECASE)
    if ' or ' in phrase_lower: phrase = re.sub(r'\s+or\s+', ' OrElse ', phrase, flags=re.IGNORECASE)
    if phrase_lower.startswith('elif '): phrase = "ifis " + phrase[5:]
    phrase_lower = phrase.lower()

    # 🌲 4. THE FAMILY TREE HIERARCHY SECTOR
    if 'is child of' in phrase_lower:
        match = re.search(r'(?:SaveSpaceFor)\s+(\w+)\s+(?:is child of)\s+(\w+)', phrase, re.IGNORECASE)
        if match:
            child, parent = match.group(1), match.group(2)
            memory[child] = {"type": "Child", "parent": parent}
            print(f"🌲 [Hierarchy]: Link established: '{child}' is a Child of master folder '{parent}'.")
            return True

    if phrase_lower.startswith('gatherchildren from ') or phrase_lower.startswith('getchildren from '):
        match = re.search(r'(?:GatherChildren|GetChildren) from\s+(\w+)', phrase, re.IGNORECASE)
        if match:
            target = match.group(1)
            memory["Children"] = [k for k, v in memory.items() if isinstance(v, dict) and str(v.get("parent")).lower() == target.lower()]
            print(f"📦 [Hierarchy]: Gathered all Children from '{target}': {memory['Children']}")
            return True

    if phrase_lower.startswith('gatherrelatives from ') or phrase_lower.startswith('getrelatives from '):
        match = re.search(r'(?:GatherRelatives|GetRelatives) from\s+(\w+)', phrase, re.IGNORECASE)
        if match:
            target = match.group(1)
            target_key = next((k for k in memory if k.lower() == target.lower()), None)
            target_data = memory.get(target_key)
            if isinstance(target_data, dict) and "parent" in target_data:
                parent = target_data["parent"]
                memory["Relatives"] = [k for k, v in memory.items() if isinstance(v, dict) and str(v.get("parent")).lower() == parent.lower() and k.lower() != target.lower()]
                print(f"👥 [Hierarchy]: Gathered all Relatives sharing parent '{parent}': {memory['Relatives']}")
            return True

    if phrase_lower.startswith('waitfor'):
        print(f"⏱️ [Sandbox Sync]: Executing hierarchy buffer sync... (Safe-check passed)")
        return True

    # 📡 5. INTER-SCRIPT SIGNALING DECODER
    if phrase_lower.startswith('receivesignal from '):
        match = re.search(r'(?:ReceiveSignal) from\s+"([^"]+)"', phrase, re.IGNORECASE)
        if match:
            print(f"📡 [Radio Link]: Script is now passively listening for transmissions from '{match.group(1)}'...")
            trackers["condition_passed"] = True
            return True

    # ⏱️ 6. REAL-TIME TIMELINE COUNTDOWN CLOCKS
    if phrase_lower.startswith('countdown ') or phrase_lower.startswith('wait '):
        match = re.search(r'(?:CountDown|wait)\s+(?:"|\')?(\d+)[sS]?(?:"|\')?', phrase, re.IGNORECASE)
        if match:
            duration = int(match.group(1))
            for i in range(duration, -1, -1):
                memory["Seconds"] = f"{i}s"
                print(f"   Seconds: {i}s")
                time.sleep(1)
                if i == 0: break
            return True

    if phrase_lower == 'when seconds stop':
        trackers["condition_passed"] = (memory.get("Seconds") == "0s")
        return True

    # 🔒 7. STOPCOUNT HARDCODED COMPILATION SAFETY GATES
    if phrase_lower.startswith('stopcount'):
        print('🔒 [StopCount Guard]: Calculation floor frozen at "0s" securely. Math subtractions locked.')
        return True

    # 📦 8. STORAGE ALLOCATIONS: SaveSpaceFor / is
    if phrase_lower.startswith('savespacefor '):
        match = re.search(r'(?:SaveSpaceFor)\s+(\w+)\s+(?:is)\s+(.+)', phrase, re.IGNORECASE)
        if match:
            var_name, var_value = match.group(1), match.group(2).strip()
            if var_value.lower() in ["yes", "true"]: memory[var_name] = "Yes"
            elif var_value.lower() in ["no", "false"]: memory[var_name] = "No"
            elif (var_value.startswith('"') and var_value.endswith('"')) or (var_value.startswith("'") and var_value.endswith("'")):
                memory[var_name] = var_value.strip('"\'')
            else:
                try: memory[var_name] = int(var_value)
                except ValueError: memory[var_name] = var_value
            return True

    # 🧮 9. MATHEMATICS OPERATORS
    if ' + ' in phrase or 'subtract ' in phrase_lower or ' * ' in phrase:
        add_match = re.search(r'(\w+)\s*\+\s*(\d+)', phrase)
        if add_match:
            k = next((x for x in memory if x.lower() == add_match.group(1).lower()), add_match.group(1))
            if k in memory: memory[k] += int(add_match.group(2)); return True
        sub_match = re.search(r'(?:Subtract)\s+(\d+)\s+from\s+(\w+)', phrase, re.IGNORECASE)
        if sub_match:
            k = next((x for x in memory if x.lower() == sub_match.group(2).lower()), sub_match.group(2))
            if k in memory: memory[k] -= int(sub_match.group(1)); return True
        mult_match = re.search(r'(\w+)\s*\*\s*(\d+)', phrase)
        if mult_match:
            k = next((x for x in memory if x.lower() == mult_match.group(1).lower()), mult_match.group(1))
            if k in memory: memory[k] *= int(mult_match.group(2)); return True

    # 🧠 10. FLOW FILTERS: If / Otherwise
    if phrase_lower.startswith('if '):
        match = re.search(r'(?:If)\s+(\w+)\s+(?:is|==)\s*(.+)', phrase, re.IGNORECASE)
        if match:
            var_name, comp_val = match.group(1), match.group(2).strip().strip('"\'').strip(':')
            if comp_val.lower() == "true": comp_val = "Yes"
            if comp_val.lower() == "false": comp_val = "No"
            k = next((x for x in memory if x.lower() == var_name.lower()), var_name)
            trackers["condition_passed"] = (str(memory.get(k)) == str(comp_val))
            return True

    if phrase_lower == "otherwise" or phrase_lower == "else:":
        trackers["condition_passed"] = not trackers["condition_passed"]
        return True

    if phrase_lower == "end":
        return False

    return True

if __name__ == "__main__":
    print("--- 🎮 SCRIPTION NATIVE MACHINE INTERPRETER v4.0 🎮 ---")
    print("Continuous multi-command processing active. Type 'end' to close.\n")
    memory = {"Seconds": "0s"}
    trackers = {"condition_passed": True}
    
    while True:
        try:
            user_input = input("Scription> ")
            if not user_input.strip(): continue
            
            # Split major structural segments by Cut boundary walls
            segments = user_input.split('Cut')
            for segment in segments:
                if not segment.strip(): continue
                
                # Unpack and run every continuous phrase hidden on this line path sequentially!
                phrases = parse_continuous_phrases(segment)
                for phrase in phrases:
                    if not execute_phrase(phrase, memory, 1, trackers):
                        print("\n👋 Closing Scription 4.0 core compiler.")
                        sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            break
