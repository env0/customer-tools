import random
import string

def randomize_workspace_name(
    prefix='env0', 
    length=6,
):
    random_part = ''.join(
        random.choices(
            string.ascii_lowercase + string.digits, 
            k=length,
        )
    )
    return f'{prefix}{random_part}'
