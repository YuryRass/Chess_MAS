import getopt
import sys
import asyncio
import aioconsole as aio
from console.command import CommandEnum, get_command

from environment.env_state import (
    EnvState,
    EnvStateType,
    IdleEnvState,
    ReadyEnvState,
    RunningEnvState,
    FinishEnvState,
)
from environment.environment import Environment

from utils.board_visualizer import board_visualizer
from utils.piece_storage import PieceStorage
from notation.fen_notation_parser import FenNotationParser


class ConsoleInterface:
    """Интерфейс консоли"""
    def __init__(self):
        self.env: Environment | None = None
        self.parser = FenNotationParser()

    def run(self):
        """Запуск приложения с передачей аргументов

        Raises:
            getopt.GetoptError: ошибка в переданных аргументах
        """
        argumentList = sys.argv[1:]
        options = "f:"
        long_options = ["fen"]
        try:
            fen = ""
            arguments, _ = getopt.getopt(
                argumentList,
                options,
                long_options,
            )
            if len(arguments) > 1:
                raise getopt.GetoptError("Problems in input args")
            if not arguments:
                fen = "Q6Q/8/8/3QQ3/3QQ3/8/8/Q6Q"
                # fen = '8/8/5B2/8/B1Q2B2/8/1Q2Q3/Q7'
                # fen = '8/3N4/5K2/8/3R4/NB3B2/3R4/1Q3Q2'
            else:
                fen = arguments[0][1]
            storage = PieceStorage(is_standart=True)
            board = self.parser.parse(fen, storage)
            self.env = Environment(
                board,
                self.environment_callback,
                None,
            )
            asyncio.run(self.control_loop())
        except getopt.error as err:
            print(str(err))

    async def control_loop(self) -> None:
        if self.env is not None:
            await self.env.initialize()
        else:
            raise NotImplementedError("Environment not initialized")

        while True:
            command = await aio.ainput()
            match get_command(command):
                case CommandEnum.STEP:
                    await self.env.step()
                case CommandEnum.STOP:
                    await self.env.stop()
                case CommandEnum.AUTO:
                    asyncio.create_task(self.env.run())
                case CommandEnum.NONE:
                    ...

    def environment_callback(self, state: EnvState) -> None:
        match state.state_type:
            case EnvStateType.IDLE:
                if isinstance(state, IdleEnvState):
                    print("Environment idle")
            case EnvStateType.READY:
                if isinstance(state, ReadyEnvState):
                    print(state.new_events)
                    print(board_visualizer(state.board))
                    print(f"Conflicts: {len(state.board.get_conflicts())}")
            case EnvStateType.RUNNING:
                if isinstance(state, RunningEnvState):
                    print("Environment running")
                    print(board_visualizer(state.board))
                    print(f"Conflicts: {len(state.board.get_conflicts())}")
            case EnvStateType.FINISH:
                if isinstance(state, FinishEnvState):
                    print("Environment finished")
                    print(board_visualizer(state.board))
                    print(self.parser.serialize(state.board))
                    print(
                        f"Epoch number: {state.epoch_number},"
                        f"Conflicts: {len(state.board.get_conflicts())}"
                    )
                    loop = asyncio.get_running_loop()
                    loop.stop()
