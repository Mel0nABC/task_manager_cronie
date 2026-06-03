import os
import stat


class cronie_task:

    def __init__(
        self: str,
        minut: str,
        hour: str,
        day: str,
        month: str,
        week_day: str,
        command: str,
        status: bool,
    ) -> dict:
        if not minut == "*":
            minut = int(minut)
            if minut < 0 or minut > 59:
                raise ValueError(
                    {"error": "Los minutos deben ser un número del 0 al 59."}
                )
        self.minut = minut
        if not hour == "*":
            hour = int(hour)
            if hour < 0 or hour > 23:
                raise ValueError({"error": ("Las horas están "
                                            "comprendidas de 0h a 23h")})
        self.hour = hour
        if not day == "*":
            day = int(day)
            if day < 1 or day > 31:
                raise ValueError({"error": ("Los días están"
                                            " comprendidos de 1 a 31")})
        self.day = day

        if not month == "*":
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError({"error": ("Los meses están"
                                            " comprendidos de 1 a 12.")})
        self.month = month
        if not week_day == "*":
            week_day = int(week_day)
            if week_day < 0 or week_day > 7:
                raise ValueError(
                    {
                        "error": "Los días de la semana están "
                        "comprendidos de 1 a 7. Siendo domingo 0."
                    }
                )
        self.week_day = week_day

        self.status = status
        if command:
            self.command = command
        else:
            raise ValueError(
                {"error": "El comando no puede estar en blanco o ser None."}
            )

        try:
            with open(command):
                modo = os.stat(command).st_mode
                executable = bool(modo & stat.S_IXUSR)
                if not executable:
                    raise ValueError(
                        {
                            "error": (
                                "El archivo del comando,"
                                " no tiene permiso de ejecución."
                            )
                        }
                    )
        except FileNotFoundError:
            raise ValueError(
                {
                    "error": (
                        "El comando que ha elegido,"
                        " no existe, archivo no encontrado."
                    )
                }
            )


# 🛠️ Sintaxis básica del crontab

# *     *     *     *     *     comando
# |     |     |     |     |
# |     |     |     |     +----- Día de la semana (0 - 7) (domingo = 0 o 7)
# |     |     |     +----------- Mes (1 - 12)
# |     |     +----------------- Día del mes (1 - 31)
# |     +----------------------- Hora (0 - 23)
# +----------------------------- Minuto (0 - 59)


# cron = cronie_task("b",4,3,4,2,"/usr/bin/ls", True)
