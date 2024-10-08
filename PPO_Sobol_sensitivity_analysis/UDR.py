from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
import copy


class UDRCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: Verbosity level: 0 for no output, 1 for info messages, 2 for debug messages
    """

    def __init__(self, env, range_value, verbose: int = 0, mass=None):
        super().__init__(verbose)
        # Those variables will be accessible in the callback
        # (they are defined in the base class)
        # The RL model
        # self.model = None  # type: BaseAlgorithm
        # An alias for self.model.get_env(), the environment used for training
        # self.training_env # type: VecEnv
        # Number of time the callback was called
        # self.n_calls = 0  # type: int
        # num_timesteps = n_envs * n times env.step() was called
        # self.num_timesteps = 0  # type: int
        # local and global variables
        # self.locals = {}  # type: Dict[str, Any]
        # self.globals = {}  # type: Dict[str, Any]
        # The logger object, used to report things in the terminal
        # self.logger # type: stable_baselines3.common.logger.Logger
        # Sometimes, for event callback, it is useful
        # to have access to the parent object
        # self.parent = None  # type: Optional[BaseCallback]
        self.training_env = env
        self.range = range_value
        self.masses = copy.deepcopy(self.training_env.sim.model.body_mass)
        if mass in [1,2,3]:
            self.min = mass+1
            self.max = mass+2
        else:
            self.min = 2
            self.max = 5

    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """
        np.random.seed(42)

    def _on_rollout_start(self) -> None:
        """
        A rollout is the collection of environment interaction
        using the current policy.
        This event is triggered before collecting new samples.
        """
        pass

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: If the callback returns False, training is aborted early.
        """
        # print(self.locals.get('done'))
        if self.locals.get("done"):
            for i in range(self.min, self.max):
                min_value = self.masses[i] - self.range if self.masses[i] - self.range > 0 else 0.5
                max_value = self.masses[i] + self.range
                self.training_env.envs[0].sim.model.body_mass[i] = np.random.uniform(min_value, max_value)
            if self.verbose > 0:
                print(self.training_env.envs[0].sim.model.body_mass)

        return True

    def _on_rollout_end(self) -> None:
        """
        This event is triggered before updating the policy.
        """
        pass

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        pass
