import pygame

animations = {}

def register_animation(anim_id, frames, frame_duration, loop=True):
    animations[anim_id] = {
        "frames": frames,
        "frame_duration": frame_duration,
        "loop": loop,
        "current_frame": 0,
        "elapsed_time": 0,
        "is_playing": True,
        "is_finished": False
    }

def play_animation(anim_id):
    if anim_id in animations:
        animation = animations[anim_id]
        animation["is_playing"] = True
        animation["is_finished"] = False
        animation["current_frame"] = 0
        animation["elapsed_time"] = 0.0

def stop_animation(anim_id):
    if anim_id in animations:
        animations[anim_id]["is_playing"] = False
        animations[anim_id]["is_finished"] = True
        animations[anim_id]["current_frame"] = 0
        animations[anim_id]["elapsed_time"] = 0.0

def reset_animation(anim_id):
    if anim_id in animations:
        animations[anim_id]["current_frame"] = 0
        animations[anim_id]["elapsed_time"] = 0.0
        animations[anim_id]["is_finished"] = False

def update_animation(anim_id, delta_time):
    if anim_id in animations:
        animation = animations[anim_id]

        if animation["is_playing"] and not animation["is_finished"]:
            animation["elapsed_time"] += delta_time

            if animation["elapsed_time"] >= animation["frame_duration"]:
                animation["elapsed_time"] -= animation["frame_duration"]
                animation["current_frame"] += 1

                if animation["current_frame"] >= len(animation["frames"]):
                    if animation["loop"]:
                        animation["current_frame"] = 0
                    else:
                        animation["current_frame"] = len(animation["frames"]) - 1
                        animation["is_finished"] = True
                        animation["is_playing"] = False

def update_all(delta_time):
    for anim_id in animations:
        if animations[anim_id]["is_playing"]:
            update_animation(anim_id, delta_time)

def get_current_frame(anim_id):
    if anim_id in animations:
        animation = animations[anim_id]
        return animation["frames"][animation["current_frame"]]
    return None

def draw_animation(render_surface, anim_id, position, is_flipped=False):
    current_frame = get_current_frame(anim_id)
    if current_frame:
        render_surface.blit(pygame.transform.flip(current_frame, is_flipped, False), position)

def is_playing(anim_id):
    return anim_id in animations and animations[anim_id]["is_playing"]

def is_finished(anim_id):
    return anim_id in animations and animations[anim_id]["is_finished"]
    