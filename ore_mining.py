"""
Minecraft Automation Script (Sanitized for GitHub)

This script demonstrates:
- Entity scanning and filtering
- Smooth rotation (yaw/pitch math)
- Movement toward points of interest
- Interaction logic (punch/use)
- Event queue handling
- Basic API integration (Telegram notifications placeholder)

Some data has been sanitized for public sharing (tokens, chat IDs, and exact NBT strings).
"""


# IMPORTS
import minescript
import time
import math
import random
import queue
import requests
from datetime import datetime



# CONFIG
TARGET_ENTITY = "entity.minecraft.armor_stand"
EYE_HEIGHT = 1.62

# Example coordinates (POI) for demonstration
POI = [
    (678.5, 96, -268.7),
    (678, 96, -291.5),
    (676.5, 96, -293.5),
    (642.5, 94, -293.5),
]

ORE_TYPE = "Ore" # Example interaction type
TP_BACK = True

# Telegram placeholders to demonstrate API integration
BOT_TOKEN = "TELEGRAM_TOKEN_HERE"
CHAT_ID = 12345678990



# TELEGRAM NOTIFICATIONS
def send_notification(message):
    """Send a Telegram message (bot token and chat ID are placeholders)."""
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)



# HELPERS
def normalize(angle):
    """Normalize an angle between -180 and 180 degrees."""
    
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def lookat(x, y, z):
    """Smoothly rotate player toward a target coordinate."""
    
    px, py, pz = minescript.player_position()
    ex, ey, ez = px, py + EYE_HEIGHT, pz

    dx = x - ex
    dy = y - ey
    dz = z - ez

    target_yaw = -math.degrees(math.atan2(dx, dz))
    target_pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))

    start_yaw, start_pitch = minescript.player_orientation()
    delta_yaw = normalize(target_yaw - start_yaw)
    delta_pitch = normalize(target_pitch - start_pitch)

    steps = random.randint(3, 6)
    for i in range(steps):
        frac = (i + 1) / steps
        ease = 0.5 - 0.5 * math.cos(math.pi * frac)
        yaw = start_yaw + delta_yaw * ease + random.uniform(-0.05, 0.05)
        pitch = start_pitch + delta_pitch * ease + random.uniform(-0.05, 0.05)
        minescript.player_set_orientation(yaw, pitch)
        time.sleep(random.uniform(0.003, 0.008))


def entity_still_exists(entid):
    """Check if a specific entity still exists in the world."""
    
    for e in minescript.get_entities():
        if e.id == entid:
            return True
    return False


def scan_entities(max_found=4):
    """Return nearby entities of the target type"""
    
    found = []
    adjust = 0
    for e in minescript.get_entities(nbt = True, max_distance = 4.5):
        
      if getattr(e, "type", None) == TARGET_ENTITY and "eyJ0aW1lc3RhbXAiOjE1Mjc1MDQyMTkzNzUsInB" in e.nbt:
        found.append((e.position[0] + adjust, e.position[1] + adjust, e.position[2] + adjust, e.id))
        
        if len(found) >= max_found:
            break
    return found


def distance_to_entity(entity):
    """Calculate distance from player to an entity."""
    
    px, py, pz = minescript.player_position()
    dx = entity[0] - px
    dy = entity[1] - py
    dz = entity[2] - pz
    return math.sqrt(dx*dx + dy*dy + dz*dz)


# INTERACTION LOGIC
def speed():
    """An action giving the player speed when ran."""
    
    px, py, pz = minescript.player_position()
    lookat(px, py + 20, pz)
    minescript.player_inventory_select_slot(0)
    minescript.player_press_attack(True)
    time.sleep(0.05)
    minescript.player_press_attack(False)
    time.sleep(0.15)
    minescript.player_press_attack(True)
    time.sleep(0.05)
    minescript.player_press_attack(False)
    time.sleep(0.15)
    minescript.player_press_attack(True)
    time.sleep(0.05)
    minescript.player_press_attack(False)
    time.sleep(2)
    minescript.player_inventory_select_slot(2)


def punch_entity(x, y, z, entid, smooth=True):
    """Interact with an entity until it disappears."""
    
    # Parameters
    adjust = 1.3
    stuck_check = 15
    stuck_sent = False
    
    with minescript.tick_loop:
        if smooth:
            lookat(x, y, z)
        else:
            minescript.player_look_at(x, y, z)

        dist = distance_to_entity((x, y, z))
        
        # Walk toward entity if too far
        if dist > 4.5:
            minescript.player_press_forward(True)
            minescript.player_press_jump(True)
            while True:
                dist = distance_to_entity((x, y, z))
                
                if dist <= 3:
                    minescript.player_press_jump(False)
                    minescript.player_press_forward(False)
                    break

                
                if smooth:
                    lookat(x, y, z)
                time.sleep(0.005)
                
            if smooth:
                lookat(x, y, z)

        # attack entity
        
        if ORE_TYPE == "Ingot":
            minescript.player_press_attack(True)
            lookat(x, y + (adjust / 2), z)
            minescript.player_press_attack(True)
            lookat(x, y + adjust, z)
            minescript.player_press_attack(True)
            lookat(x, y + adjust + .8, z)
            minescript.player_press_attack(True)
            minescript.player_press_attack(False)
            
        else:
            minescript.player_press_use(True)
            lookat(x, y + (adjust / 2), z)
            lookat(x, y + adjust, z)
            lookat(x, y + adjust + .8, z)
            minescript.player_press_use(False)

        check_stuck = time.time()
        # wait until entity disappears
        while entity_still_exists(entid):
            time.sleep(0.01)
            if (time.time() - check_stuck) > stuck_check and not stuck_sent:
                stuck_sent = True
                send_notification(f"I missed T-T. HELPPPP!!!")


def pick_closest(entities):
    """Select the closest entity to the player."""
    
    px, py, pz = minescript.player_position()
    best = None
    best_dist = float("inf")
    
    for e in entities:
        dx, dy, dz = e[0]-px, e[1]-py, e[2]-pz
        dist = dx*dx + dy*dy + dz*dz
        
        if dist < best_dist:
            best_dist = dist
            best = e
            
    return best




def main():
    # Parameters
    precision = 0.85
    shift_range = precision + 4
    pick_range = shift_range + 5
    walk_y = 96
    speed_duration = 180
    stuck_check = 15
    stuck_sent = False
    start_time = time.time()
    stopwatch = time.time()
    no_durability = False
    eq = minescript.EventQueue()
    eq.register_chat_listener()
    
    # Logic
    speed()
    while not no_durability:
      for coord in POI:
        px, py, pz = minescript.player_position()
        minescript.player_inventory_select_slot(0)
        check_stuck = time.time()
        
        # Walk to Point of Interest
        while not(coord[0] <= px + precision and coord[0] > px - precision and coord[2] <= pz + precision and coord[2] > pz - precision):
            px, py, pz = minescript.player_position()
            lookat(coord[0], coord[1] + 1.5, coord[2])
            minescript.player_press_forward(True)
            
            if coord[1] != walk_y:
                minescript.player_press_jump(True)
                
            if coord[0] <= px + shift_range and coord[0] > px - shift_range and coord[2] <= pz + shift_range and coord[2] > pz - shift_range:
                minescript.player_press_sneak(True)
                
            if coord[0] <= px + pick_range and coord[0] > px - pick_range and coord[2] <= pz + pick_range and coord[2] > pz - shift_range:
                minescript.player_inventory_select_slot(2)
                
            if (time.time() - check_stuck) > stuck_check and not stuck_sent:
                stuck_sent = True
                send_notification(f"I'm stuck T-T!!! Help!!!")
        
        # Reset        
        stuck_sent = False
        minescript.player_press_sneak(False)
        minescript.player_press_jump(False)
        minescript.player_press_forward(False)
        time.sleep(0.1)
        minescript.player_inventory_select_slot(2)
        
        entities_to_attack = scan_entities()

        while entities_to_attack:
            target = pick_closest(entities_to_attack)
            
            if target:
                x, y, z, entid = target
                punch_entity(x, y, z, entid)
                entities_to_attack.remove(target)
                
                # Check durability only if TP_BACK is true
                while TP_BACK:
                    try:
                        event = eq.get(timeout=0)
                    except queue.Empty:
                        break

                    if "0 durability left!" in event.message.lower():
                        no_durability = True
                        
                        minescript.player_inventory_select_slot(3)
                        minescript.player_press_use(True)
                        minescript.player_press_use(False)
                        
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        timetaken = time.time() - stopwatch
                        send_notification(f"Mining finished!\nTimestamp: {now}\nTime Taken: {timetaken}")
                        
                        break  # Stop checking chat events

                if no_durability:
                    break  # Stop attacking if durability is gone
                
                time.sleep(random.uniform(0.05, 0.1))
                
        if no_durability:
            break
        
        if (time.time() - start_time) > speed_duration:
            start_time = time.time()
            speed()

main()
