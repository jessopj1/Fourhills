from pathlib import Path
from typing import Optional
from fourhills.exceptions import FourhillsSettingStructureError


class Setting:
    """Represents the campaign setting directory tree."""

    CONFIG_FILENAME = "fh_setting.yaml"
    DIRNAMES = {"world": "world", "monsters": "monsters", "npcs": "npcs"}

    def __init__(self):
        self.root = self.find_root()
        self.pane_width = 56
        self.panes = 2
        self.column_width = 60

    @staticmethod
    def find_root() -> Optional[Path]:
        """Find the root of the setting.

        Notes
        -----
        Ascends the directory tree looking for `SETTING_CONFIG_FILENAME`.

        Returns
        -------
        pathlib.Path or None
            The setting's root directory, or None if the file wasn't found
        """
        # Get the current working directory and resolve any symlinks etc.
        current_dir = Path.cwd().resolve()
        # While we can still ascend
        while current_dir != current_dir.parent:
            # See if the settings file exists
            if (current_dir / Setting.CONFIG_FILENAME).is_file():
                # Make sure the require directories are there
                for directory_name in Setting.DIRNAMES.values():
                    if not (current_dir / directory_name).is_dir():
                        raise FourhillsSettingStructureError(
                            f"Setting root does not contain {directory_name} directory."
                        )
                return current_dir
            current_dir = current_dir.parent
        # If the root directory wasn't found, return None
        return None

    @property
    def world_dir(self):
        return self.root / self.DIRNAMES["world"]

    @property
    def monsters_dir(self):
        return self.root / self.DIRNAMES["monsters"]

    @property
    def npcs_dir(self):
        return self.root / self.DIRNAMES["npcs"]
